"""
Geographic Footprint & Service Area Detector (Phase 05).
Extracts primary headquarters, service cities/states, and office counts.
"""

import re
from src.business_intelligence.models import GeographicFootprint
from src.contact_discovery.models import BusinessAddress
from src.enrichment.parser import HTMLParserDocument


class GeographicDetector:
    """Detects service areas, office locations count, states served, and primary headquarters."""

    def detect_geography(
        self,
        doc: HTMLParserDocument | None,
        addresses: list[BusinessAddress] | None = None
    ) -> GeographicFootprint:
        """
        Extracts GeographicFootprint model from address data, footer text, and page content.
        """
        footprint = GeographicFootprint()
        service_areas: set[str] = set()
        states_served: set[str] = set()

        if addresses:
            footprint.office_locations_count = max(1, len(addresses))
            first_addr = addresses[0]
            if first_addr.city or first_addr.state:
                hq_bits = [b for b in [first_addr.city, first_addr.state, first_addr.country] if b]
                footprint.primary_headquarters = ", ".join(hq_bits)
                if first_addr.city:
                    service_areas.add(first_addr.city)
                if first_addr.state:
                    states_served.add(first_addr.state)

        if doc and doc.soup:
            text = doc.soup.get_text(separator=" ")

            # Pattern: "Serving [City1], [City2], and [City3]" or "Service Areas: City1, City2"
            match = re.search(r"(?:serving|service areas?|locations?):\s*([A-Za-z0-9\s,–-]+)", text, re.IGNORECASE)
            if match:
                areas_str = match.group(1)
                tokens = [t.strip() for t in re.split(r"[,&|•\n]", areas_str) if t.strip()]
                for tok in tokens[:6]:
                    if 2 <= len(tok) <= 30 and not any(digit in tok for digit in "0123456789"):
                        service_areas.add(tok.title())

            # Detect US / AU / UK state acronyms
            state_matches = re.findall(r"\b(NSW|VIC|QLD|WA|SA|TAS|ACT|NT|CA|TX|NY|FL|IL|PA|OH|GA|NC|MI)\b", text)
            for st in state_matches:
                states_served.add(st.upper())

        footprint.service_areas = list(service_areas)[:8]
        footprint.states_served = list(states_served)[:6]

        if not footprint.primary_headquarters and footprint.service_areas:
            footprint.primary_headquarters = footprint.service_areas[0]

        return footprint
