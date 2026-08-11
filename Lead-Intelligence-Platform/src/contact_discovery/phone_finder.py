"""
Phone Intelligence Finder Module.
Extracts Australian and international phone numbers, normalizes to E.164 format, classifies number types, and assigns confidence.
"""

import re
from src.contact_discovery.models import ConfidenceLevel, ContactPhone, PhoneCategory
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class PhoneFinder:
    """Discovers, normalizes, and classifies business phone numbers."""

    # Australian Phone RegEx Patterns
    TEL_LINK_REGEX = re.compile(r'tel:\+?([0-9\s()-]{8,20})')
    AU_PHONE_REGEX = re.compile(
        r'(?:\+?61\s*\(?0?\)?|\(?0[2378]\)?|\(?04\d{2}\)?)\s*\d{3,4}\s*\d{3,4}|1[38]00\s*\d{3}\s*\d{3}|13\s*\d{2}\s*\d{2}'
    )

    def find_phones(self, doc: HTMLParserDocument, source_url: str = "") -> list[ContactPhone]:
        """
        Extracts, normalizes, and classifies phone numbers from document.
        """
        from src.utils.phone_normalizer import PhoneNormalizer, SharedPhoneCategory

        raw_text = doc.soup.get_text()

        # Extract tel: links first
        tel_links = []
        for a in doc.soup.find_all("a", href=True):
            href = str(a.get("href"))
            if href.startswith("tel:"):
                clean = href.replace("tel:", "").strip()
                if clean:
                    tel_links.append(clean)

        text_matches = self.AU_PHONE_REGEX.findall(raw_text)
        combined_candidates = set(tel_links + text_matches)

        results = []
        seen_keys = set()

        for raw_phone in combined_candidates:
            e164, formatted, shared_cat = PhoneNormalizer.normalize(raw_phone)
            dedup_key = e164 or formatted

            if not dedup_key or dedup_key in seen_keys:
                continue

            seen_keys.add(dedup_key)

            # Map SharedPhoneCategory to PhoneCategory enum
            cat_map = {
                SharedPhoneCategory.MOBILE: PhoneCategory.MOBILE,
                SharedPhoneCategory.LANDLINE: PhoneCategory.LANDLINE,
                SharedPhoneCategory.TOLL_FREE: PhoneCategory.TOLL_FREE,
            }
            category = cat_map.get(shared_cat, PhoneCategory.UNKNOWN)

            is_tel = any(raw_phone in link for link in tel_links)
            is_contact = "contact" in source_url.lower()
            confidence = ConfidenceLevel.HIGH if (is_tel or is_contact) else ConfidenceLevel.MEDIUM

            results.append(
                ContactPhone(
                    raw_number=raw_phone,
                    e164_number=e164,
                    formatted_number=formatted or e164 or raw_phone,
                    category=category,
                    country_code="AU",
                    source_url=source_url,
                    confidence=confidence
                )
            )

        return results
