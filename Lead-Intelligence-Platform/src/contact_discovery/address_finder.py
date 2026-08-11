"""
Physical Business Address Finder Module.
Extracts and parses Australian physical street addresses, suburb/city, state, postal code, and country.
"""

import re
from src.contact_discovery.models import BusinessAddress, ConfidenceLevel
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class AddressFinder:
    """Extracts physical business address blocks from DOM elements and text."""

    AU_STATE_REGEX = re.compile(
        r'(\d+[\w\s,-]+?),\s*([A-Za-z\s]+?)\s+(NSW|VIC|QLD|WA|SA|TAS|ACT|NT)\s+(\d{4})',
        re.IGNORECASE
    )

    def find_addresses(self, doc: HTMLParserDocument, source_url: str = "") -> list[BusinessAddress]:
        """
        Scans address tags, footer blocks, and document text for physical address matches.
        """
        results = []
        seen_raw = set()

        # 1. Inspect explicit <address> tags
        for addr_tag in doc.soup.find_all("address"):
            txt = addr_tag.get_text(separator=" ", strip=True)
            if txt and txt not in seen_raw:
                seen_raw.add(txt)
                parsed_addr = self._parse_address_string(txt, source_url, ConfidenceLevel.HIGH)
                results.append(parsed_addr)

        # 2. Inspect text regex patterns
        raw_text = doc.soup.get_text()
        for match in self.AU_STATE_REGEX.finditer(raw_text):
            full_match = match.group(0).strip()
            if full_match not in seen_raw:
                seen_raw.add(full_match)
                street = match.group(1).strip()
                city = match.group(2).strip()
                state = match.group(3).upper()
                postcode = match.group(4)

                results.append(
                    BusinessAddress(
                        raw_address=full_match,
                        street=street,
                        city=city,
                        state=state,
                        postal_code=postcode,
                        country="Australia",
                        source_url=source_url,
                        confidence=ConfidenceLevel.HIGH
                    )
                )

        return results

    def _parse_address_string(self, raw_str: str, source_url: str, confidence: ConfidenceLevel) -> BusinessAddress:
        """Parses address fields from raw text string."""
        match = self.AU_STATE_REGEX.search(raw_str)
        if match:
            return BusinessAddress(
                raw_address=raw_str,
                street=match.group(1).strip(),
                city=match.group(2).strip(),
                state=match.group(3).upper(),
                postal_code=match.group(4),
                country="Australia",
                source_url=source_url,
                confidence=confidence
            )

        return BusinessAddress(
            raw_address=raw_str,
            country="Australia",
            source_url=source_url,
            confidence=confidence
        )
