"""
Years-In-Business Estimator (Phase 05).
Detects founding year and calculates company age in years.
"""

import datetime
import re
from src.business_intelligence.validators import BusinessIntelligenceValidator
from src.enrichment.parser import HTMLParserDocument


class YearsInBusinessDetector:
    """Estimates founding year and years in business from 'Founded in XYZ', copyright dates, and history text."""

    CURRENT_YEAR = 2026

    def detect_years(self, doc: HTMLParserDocument | None) -> tuple[int | None, int | None]:
        """
        Returns (founded_year, years_in_business).
        """
        if not doc or not doc.soup:
            return (None, None)

        text = doc.soup.get_text(separator=" ")

        # 1. Explicit patterns: "Founded in 2004", "Established in 1998", "Since 1985"
        match = re.search(r"\b(?:founded|established|since|serving since)\s+(?:in\s+)?(18\d{2}|19\d{2}|20[0-2]\d)\b", text, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            if 1800 <= year <= self.CURRENT_YEAR:
                return (year, self.CURRENT_YEAR - year)

        # 2. Pattern: "Over 20 years of experience", "25 years in business"
        exp_match = re.search(r"\b(?:over|more than|celebrating)?\s*(\d{1,2})\+?\s*years(?:\s+of|\s+in)?\s+(?:experience|business|service)\b", text, re.IGNORECASE)
        if exp_match:
            years = int(exp_match.group(1))
            if 1 <= years <= 150:
                est_founding = self.CURRENT_YEAR - years
                return (est_founding, years)

        # 3. Copyright year fallback in footer (e.g. "© 2006-2026 Company Name")
        copy_match = re.search(r"©\s*(19\d{2}|20[0-2]\d)\s*[-–]\s*(20[0-2]\d)", text)
        if copy_match:
            start_year = int(copy_match.group(1))
            if 1900 <= start_year <= self.CURRENT_YEAR:
                return (start_year, self.CURRENT_YEAR - start_year)

        return (None, None)
