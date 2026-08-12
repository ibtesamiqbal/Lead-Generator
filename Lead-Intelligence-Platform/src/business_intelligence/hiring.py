"""
Hiring Signal Detector (Phase 05).
Detects careers pages, open job positions, and hiring slogans.
"""

import re
from urllib.parse import urljoin
from src.business_intelligence.models import HiringSignals
from src.enrichment.parser import HTMLParserDocument


class HiringSignalDetector:
    """Detects careers pages, open positions, and recruiting language."""

    def detect_hiring(self, doc: HTMLParserDocument | None, base_url: str = "") -> HiringSignals:
        """
        Returns populated HiringSignals model.
        """
        signals = HiringSignals()
        if not doc or not doc.soup:
            return signals

        # Look for careers link
        careers_link = doc.soup.find("a", href=re.compile(r"/careers|/jobs|/join-us|/work-with-us", re.IGNORECASE))
        if careers_link:
            signals.has_careers_page = True
            href = careers_link.get("href")
            if href and isinstance(href, str):
                signals.careers_page_url = urljoin(base_url, href)

        text = doc.soup.get_text(separator=" ").lower()

        if any(kw in text for kw in ["we're hiring", "now hiring", "join our team", "open positions", "careers"]):
            signals.currently_hiring = True

        # Extract open role titles mentioned in text
        roles = []
        role_matches = re.findall(r"\b(hiring\s+[a-z\s]+|open position:\s*[a-z\s]+)\b", text)
        for r in role_matches[:4]:
            roles.append(r.title())
        signals.open_roles_detected = roles

        return signals
