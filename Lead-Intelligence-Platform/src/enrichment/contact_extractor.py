"""
Contact Information Extractor Module.
Extracts emails, phone numbers (with normalization), contact page URLs, and physical address snippets.
"""

import re
from urllib.parse import urljoin
from src.enrichment.models import ContactIntelligence
from src.enrichment.parser import HTMLParserDocument

# Regex pattern matching standard public email formats
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE
)

# Regex pattern matching Australian and International phone formats
PHONE_REGEX = re.compile(
    r"(?:\+?61|0)[23478](?:[ -]?\d){8}|\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
)

# Common image or asset file extensions to filter out false positive email matches
IGNORED_EMAIL_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js", ".wixpress.com"
)


class ContactExtractor:
    """Extracts and normalizes public business contact details from HTML DOM."""

    def extract(self, doc: HTMLParserDocument, base_url: str = "") -> ContactIntelligence:
        """
        Extracts public emails, phone numbers, contact URLs, and physical address hints.
        """
        emails = self._extract_emails(doc)
        phones = self._extract_phones(doc)
        contact_urls = self._extract_contact_pages(doc, base_url)
        addresses = self._extract_address_hints(doc)

        return ContactIntelligence(
            emails=sorted(list(set(emails))),
            phone_numbers=sorted(list(set(phones))),
            contact_page_urls=sorted(list(set(contact_urls))),
            physical_addresses=sorted(list(set(addresses)))
        )

    def _extract_emails(self, doc: HTMLParserDocument) -> list[str]:
        found_emails = set()

        # 1. Inspect mailto: href links
        for link in doc.get_all_links():
            href = link["href"]
            if href.lower().startswith("mailto:"):
                raw_email = href.split("mailto:")[-1].split("?")[0].strip()
                if self._is_valid_email(raw_email):
                    found_emails.add(raw_email.lower())

        # 2. Search regex in text content
        text_content = doc.get_text_content()
        for match in EMAIL_REGEX.findall(text_content):
            if self._is_valid_email(match):
                found_emails.add(match.lower())

        return list(found_emails)

    def _is_valid_email(self, email: str) -> bool:
        if not email or len(email) < 6 or len(email) > 254:
            return False
        clean = email.lower()
        if any(clean.endswith(ext) for ext in IGNORED_EMAIL_EXTENSIONS):
            return False
        return bool(EMAIL_REGEX.match(clean))

    def _extract_phones(self, doc: HTMLParserDocument) -> list[str]:
        from src.utils.phone_normalizer import PhoneNormalizer

        found_phones = set()

        # 1. Inspect tel: href links
        for link in doc.get_all_links():
            href = link["href"]
            if href.lower().startswith("tel:"):
                raw_phone = href.split("tel:")[-1].split("?")[0].strip()
                e164, formatted, cat = PhoneNormalizer.normalize(raw_phone)
                val = e164 or formatted
                if val:
                    found_phones.add(val)

        # 2. Search text content using strict AU phone regex and E.164 normalizer
        from src.utils.phone_normalizer import AU_STRICT_PHONE_REGEX
        text_content = doc.get_text_content()
        for match in AU_STRICT_PHONE_REGEX.findall(text_content):
            e164, formatted, cat = PhoneNormalizer.normalize(match)
            val = e164 or formatted
            if val:
                found_phones.add(val)

        return list(found_phones)

    def _extract_contact_pages(self, doc: HTMLParserDocument, base_url: str) -> list[str]:
        contact_links = set()
        contact_keywords = {"contact", "contact-us", "get-in-touch", "about-us", "reach-us"}

        for link in doc.get_all_links():
            href = link["href"].lower()
            text = link["text"].lower()

            if any(kw in href or kw in text for kw in contact_keywords):
                full_url = urljoin(base_url, link["href"]) if base_url else link["href"]
                if full_url.startswith(("http://", "https://")):
                    contact_links.add(full_url)

        return list(contact_links)

    def _extract_address_hints(self, doc: HTMLParserDocument) -> list[str]:
        address_hints = set()

        # Check <address> HTML tags
        for addr_tag in doc.soup.find_all("address"):
            text = addr_tag.get_text(separator=" ", strip=True)
            if text and len(text) > 10:
                address_hints.add(text[:200])

        return list(address_hints)
