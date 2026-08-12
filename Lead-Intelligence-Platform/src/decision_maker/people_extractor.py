"""
People Extractor module for parsing person profiles from webpage DOM and structured data.
"""

import json
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag

from src.decision_maker.models import DecisionMaker
from src.decision_maker.ranking import DecisionMakerRanker
from src.decision_maker.title_normalizer import TitleNormalizer
from src.decision_maker.validators import DecisionMakerValidator
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class PeopleExtractor:
    """Extracts individual person profiles, job titles, bios, and contacts from HTML DOM."""

    # Extended CSS selectors for team layouts across modern CMSs (WordPress Elementor/Divi, Webflow, Squarespace, Wix, etc.)
    TEAM_CONTAINER_SELECTORS = [
        ".team-member", ".team_member", ".member", ".person", ".profile-card",
        ".bio-card", ".exec-card", ".staff-member", ".leadership-card", ".team-item",
        "article", ".team", ".our-team", ".author-box", ".speaker-card", ".card-person",
        ".elementor-person", ".et_pb_team_member", ".sqs-block-summary-v2", ".w-layout-grid > div",
        "table.team tr", "ul.team-list > li", "ol.team-list > li", ".team-grid > div",
        ".leadership-grid > div", ".attorney-card", ".doctor-card", ".staff-card"
    ]

    # Job title indicator regex keywords
    TITLE_INDICATORS = [
        r"\bCEO\b", r"\bCTO\b", r"\bCOO\b", r"\bCFO\b", r"\bCMO\b", r"\bCIO\b", r"\bCRO\b", r"\bCHRO\b",
        r"\bChief\b", r"\bOfficer\b", r"\bExecutive\b", r"\bFounder\b", r"\bOwner\b", r"\bPresident\b",
        r"\bDirector\b", r"\bManager\b", r"\bHead of\b", r"\bVP\b", r"\bVice President\b",
        r"\bPartner\b", r"\bLead\b", r"\bManaging Director\b", r"\bCo-Founder\b", r"\bPrincipal\b",
        r"\bDentist\b", r"\bAttorney\b", r"\bLawyer\b", r"\bSurgeon\b", r"\bConsultant\b", r"\bSpecialist\b"
    ]

    def extract_people(self, doc: HTMLParserDocument, source_url: str, is_leadership_page: bool = True) -> list[DecisionMaker]:
        """
        Extracts all valid DecisionMaker candidates from an HTML document.
        """
        extracted_people: list[DecisionMaker] = []
        if not doc or not doc.soup:
            return extracted_people

        soup = doc.soup

        # Strategy 1: Extract from Schema.org JSON-LD structured data
        try:
            json_ld_people = self._extract_from_json_ld(soup, source_url, is_leadership_page)
            extracted_people.extend(json_ld_people)
        except Exception as err:
            logger.debug(f"JSON-LD people extraction error: {err}")

        # Strategy 2: Extract from HTML team card containers
        try:
            card_people = self._extract_from_team_cards(soup, source_url, is_leadership_page)
            extracted_people.extend(card_people)
        except Exception as err:
            logger.debug(f"HTML team card extraction error: {err}")

        # Strategy 3: Fallback DOM pattern search (Heading + Title pattern)
        if not extracted_people:
            try:
                heading_people = self._extract_from_headings(soup, source_url, is_leadership_page)
                extracted_people.extend(heading_people)
            except Exception as err:
                logger.debug(f"Heading people extraction error: {err}")

        # Deduplicate candidates by normalized full name & title
        return self._deduplicate_people(extracted_people)

    def _extract_from_json_ld(self, soup: BeautifulSoup, source_url: str, is_leadership_page: bool) -> list[DecisionMaker]:
        """Extracts person objects from Schema.org JSON-LD scripts."""
        people = []
        for script in soup.find_all("script", type="application/ld+json"):
            if not script or not script.string:
                continue
            try:
                data = json.loads(script.string)
                items = data if isinstance(data, list) else [data]

                for item in items:
                    if not isinstance(item, dict):
                        continue

                    # Direct Person type
                    if item.get("@type") in ("Person", "Physician", "Attorney"):
                        person = self._parse_json_person(item, source_url, is_leadership_page)
                        if person:
                            people.append(person)

                    # Graph containing Person items
                    elif "@graph" in item and isinstance(item["@graph"], list):
                        for node in item["@graph"]:
                            if isinstance(node, dict) and node.get("@type") in ("Person", "Physician", "Attorney"):
                                person = self._parse_json_person(node, source_url, is_leadership_page)
                                if person:
                                    people.append(person)

                    # Organization with employee/founder/attorney/member
                    elif item.get("@type") in ("Organization", "LocalBusiness", "Corporation", "LegalService", "MedicalBusiness"):
                        for key in ("employee", "founder", "alumni", "member", "attorney", "physician"):
                            val = item.get(key)
                            sub_items = val if isinstance(val, list) else ([val] if val else [])
                            for sub in sub_items:
                                if isinstance(sub, dict) and sub.get("@type") in ("Person", "Physician", "Attorney"):
                                    person = self._parse_json_person(sub, source_url, is_leadership_page)
                                    if person:
                                        people.append(person)

            except Exception as err:
                logger.debug(f"Failed parsing JSON-LD script for people extraction: {err}")

        return people

    def _parse_json_person(self, item: dict, source_url: str, is_leadership_page: bool) -> DecisionMaker | None:
        """Parses a Schema.org Person JSON dictionary."""
        name = item.get("name")
        if not name or not DecisionMakerValidator.is_valid_name(str(name)):
            return None

        job_title = item.get("jobTitle") or item.get("title") or "Executive"
        bio = item.get("description")
        image = item.get("image")
        if isinstance(image, dict):
            image = image.get("url")

        email = item.get("email")
        phone = item.get("telephone")
        same_as = item.get("sameAs")
        linkedin_url = None

        if isinstance(same_as, list):
            for link in same_as:
                if isinstance(link, str) and DecisionMakerValidator.is_valid_linkedin_url(link):
                    linkedin_url = link
                    break
        elif isinstance(same_as, str) and DecisionMakerValidator.is_valid_linkedin_url(same_as):
            linkedin_url = same_as

        first_name, last_name = DecisionMakerValidator.split_full_name(str(name))
        norm_title = TitleNormalizer.normalize_title(str(job_title))
        dept = TitleNormalizer.classify_department(norm_title)
        seniority = TitleNormalizer.classify_seniority(norm_title)

        priority = DecisionMakerRanker.calculate_priority(norm_title, dept, seniority)
        confidence = DecisionMakerRanker.calculate_confidence(
            is_leadership_page=is_leadership_page,
            has_recognized_title=norm_title != "Unknown",
            has_biography=bool(bio),
            has_contact_info=bool(email or linkedin_url)
        )

        return DecisionMaker(
            full_name=str(name).strip(),
            first_name=first_name,
            last_name=last_name,
            title=str(job_title).strip(),
            normalized_title=norm_title,
            department=dept,
            seniority=seniority,
            email=str(email).strip() if isinstance(email, str) else None,
            phone=str(phone).strip() if isinstance(phone, str) else None,
            linkedin_url=linkedin_url,
            biography=str(bio).strip() if bio else None,
            image=str(image).strip() if isinstance(image, str) and DecisionMakerValidator.is_safe_url(image) else None,
            source_url=source_url,
            confidence=confidence,
            priority=priority
        )

    def _extract_from_team_cards(self, soup: BeautifulSoup, source_url: str, is_leadership_page: bool) -> list[DecisionMaker]:
        """Extracts person details from HTML cards / containers matching CSS class selectors."""
        people = []

        containers = []
        for selector in self.TEAM_CONTAINER_SELECTORS:
            matches = soup.select(selector)
            if matches and len(matches) >= 1 and len(matches) <= 100:
                containers = matches
                break

        for card in containers:
            try:
                person = self._parse_card_element(card, source_url, is_leadership_page)
                if person:
                    people.append(person)
            except Exception as err:
                logger.debug(f"Error parsing card element: {err}")

        return people

    def _parse_card_element(self, element: Tag, source_url: str, is_leadership_page: bool) -> DecisionMaker | None:
        """Extracts name, title, bio, image, and contacts from a single HTML DOM card element."""
        # 1. Find Name (h1, h2, h3, h4, strong, or .name)
        name = None
        for tag in element.find_all(["h1", "h2", "h3", "h4", "h5", "strong"]):
            candidate = tag.get_text(strip=True)
            if DecisionMakerValidator.is_valid_name(candidate):
                name = candidate
                break

        if not name:
            name_el = element.find(class_=re.compile(r"name|person-title|attorney-name", re.IGNORECASE))
            if name_el:
                candidate = name_el.get_text(strip=True)
                if DecisionMakerValidator.is_valid_name(candidate):
                    name = candidate

        if not name:
            return None

        # 2. Find Title
        title = None
        title_el = element.find(class_=re.compile(r"title|role|position|job|sub-heading", re.IGNORECASE))
        if title_el:
            candidate_title = title_el.get_text(strip=True)
            if candidate_title and candidate_title != name and len(candidate_title) < 100:
                title = candidate_title

        if not title:
            text_lines = [line.strip() for line in element.get_text(separator="\n").split("\n") if line.strip()]
            for line in text_lines:
                if line != name and any(re.search(pat, line, re.IGNORECASE) for pat in self.TITLE_INDICATORS):
                    if len(line) < 100:
                        title = line
                        break

        if not title:
            title = "Executive / Leadership"

        # 3. Find LinkedIn Profile URL
        linkedin_url = None
        for link in element.find_all("a", href=True):
            href = link["href"]
            if DecisionMakerValidator.is_valid_linkedin_url(href):
                linkedin_url = href
                break

        # 4. Find Email
        email = None
        mailto_link = element.find("a", href=re.compile(r"^mailto:", re.IGNORECASE))
        if mailto_link:
            email = mailto_link["href"].replace("mailto:", "").split("?")[0].strip()
        else:
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", element.get_text())
            if email_match:
                email = email_match.group(0)

        # 5. Find Phone
        phone = None
        tel_link = element.find("a", href=re.compile(r"^tel:", re.IGNORECASE))
        if tel_link:
            phone = tel_link["href"].replace("tel:", "").strip()

        # 6. Find Image URL (supporting lazy-loading attributes data-src, srcset, data-lazy-src, data-original)
        image_url = None
        img_tag = element.find("img")
        if img_tag:
            src = (
                img_tag.get("src") or
                img_tag.get("data-src") or
                img_tag.get("data-lazy-src") or
                img_tag.get("data-original") or
                (img_tag.get("srcset") or "").split()[0]
            )
            if src and isinstance(src, str) and not src.startswith("data:"):
                candidate_img = urljoin(source_url, src)
                if DecisionMakerValidator.is_safe_url(candidate_img):
                    image_url = candidate_img

        # 7. Find Bio
        bio = None
        bio_el = element.find(class_=re.compile(r"bio|desc|description|about|summary", re.IGNORECASE))
        if bio_el:
            bio = bio_el.get_text(strip=True)
        else:
            paragraphs = [p.get_text(strip=True) for p in element.find_all("p") if len(p.get_text(strip=True)) > 30]
            if paragraphs:
                bio = " ".join(paragraphs[:2])

        first_name, last_name = DecisionMakerValidator.split_full_name(name)
        norm_title = TitleNormalizer.normalize_title(title)
        dept = TitleNormalizer.classify_department(norm_title)
        seniority = TitleNormalizer.classify_seniority(norm_title)

        priority = DecisionMakerRanker.calculate_priority(norm_title, dept, seniority)
        confidence = DecisionMakerRanker.calculate_confidence(
            is_leadership_page=is_leadership_page,
            has_recognized_title=norm_title != "Unknown",
            has_biography=bool(bio),
            has_contact_info=bool(email or linkedin_url or phone)
        )

        return DecisionMaker(
            full_name=name.strip(),
            first_name=first_name,
            last_name=last_name,
            title=title.strip(),
            normalized_title=norm_title,
            department=dept,
            seniority=seniority,
            email=email,
            phone=phone,
            linkedin_url=linkedin_url,
            biography=bio,
            image=image_url,
            source_url=source_url,
            confidence=confidence,
            priority=priority
        )

    def _extract_from_headings(self, soup: BeautifulSoup, source_url: str, is_leadership_page: bool) -> list[DecisionMaker]:
        """Fallback extractor scanning h2/h3 tags followed immediately by job titles."""
        people = []
        headings = soup.find_all(["h2", "h3", "h4"])

        for h in headings:
            name_candidate = h.get_text(strip=True)
            if not DecisionMakerValidator.is_valid_name(name_candidate):
                continue

            next_sibling = h.find_next_sibling(["p", "span", "div", "h5"])
            title_candidate = None
            if next_sibling:
                text = next_sibling.get_text(strip=True)
                if text and any(re.search(pat, text, re.IGNORECASE) for pat in self.TITLE_INDICATORS):
                    title_candidate = text

            if title_candidate:
                first_name, last_name = DecisionMakerValidator.split_full_name(name_candidate)
                norm_title = TitleNormalizer.normalize_title(title_candidate)
                dept = TitleNormalizer.classify_department(norm_title)
                seniority = TitleNormalizer.classify_seniority(norm_title)

                priority = DecisionMakerRanker.calculate_priority(norm_title, dept, seniority)
                confidence = DecisionMakerRanker.calculate_confidence(
                    is_leadership_page=is_leadership_page,
                    has_recognized_title=norm_title != "Unknown",
                    has_biography=False
                )

                person = DecisionMaker(
                    full_name=name_candidate.strip(),
                    first_name=first_name,
                    last_name=last_name,
                    title=title_candidate.strip(),
                    normalized_title=norm_title,
                    department=dept,
                    seniority=seniority,
                    source_url=source_url,
                    confidence=confidence,
                    priority=priority
                )
                people.append(person)

        return people

    def _deduplicate_people(self, people: list[DecisionMaker]) -> list[DecisionMaker]:
        """Deduplicates extracted candidates by normalized name, merging profile fields."""
        unique_people: dict[str, DecisionMaker] = {}
        for p in people:
            key = p.full_name.lower().strip()
            clean_key = re.sub(r"\b[a-z]\.\s+", "", key)

            if clean_key not in unique_people:
                unique_people[clean_key] = p
            else:
                existing = unique_people[clean_key]
                if not existing.email and p.email:
                    existing.email = p.email
                if not existing.linkedin_url and p.linkedin_url:
                    existing.linkedin_url = p.linkedin_url
                if not existing.phone and p.phone:
                    existing.phone = p.phone
                if not existing.biography and p.biography:
                    existing.biography = p.biography
                if not existing.image and p.image:
                    existing.image = p.image
                if p.confidence > existing.confidence:
                    existing.confidence = p.confidence
                if p.priority > existing.priority:
                    existing.priority = p.priority

        return list(unique_people.values())
