"""
Company Size Estimator (Phase 05).
Estimates company size tier, employee count range, and confidence score.
"""

from src.business_intelligence.models import CompanySizeTier
from src.decision_maker.models import DecisionMaker
from src.enrichment.parser import HTMLParserDocument


class CompanySizeEstimator:
    """Estimates employee headcount range and company size tier using team size and page signals."""

    def estimate_size(
        self,
        doc: HTMLParserDocument | None,
        decision_makers: list[DecisionMaker] | None = None,
        office_count: int = 1,
        has_careers_page: bool = False
    ) -> tuple[CompanySizeTier, str, float]:
        """
        Returns (CompanySizeTier, estimated_employee_range, confidence_score).
        """
        people_count = len(decision_makers) if decision_makers else 0

        # High confidence signal from extracted decision makers
        if people_count >= 50:
            return (CompanySizeTier.ENTERPRISE, "251+", 0.90)
        elif people_count >= 15:
            return (CompanySizeTier.MID_MARKET, "51-250", 0.85)
        elif people_count >= 5:
            return (CompanySizeTier.SMALL_BUSINESS, "11-50", 0.80)

        # Multi-office signal
        if office_count >= 5:
            return (CompanySizeTier.ENTERPRISE, "251+", 0.80)
        elif office_count >= 2:
            return (CompanySizeTier.MID_MARKET, "51-250", 0.70)

        # Content signals
        if doc and doc.soup:
            text = doc.soup.get_text(separator=" ").lower()
            if any(term in text for term in ["global office", "fortune 500", "over 10,000 employees", "worldwide locations"]):
                return (CompanySizeTier.ENTERPRISE, "251+", 0.85)
            if any(term in text for term in ["over 100 employees", "over 200 staff", "growing team of 50"]):
                return (CompanySizeTier.MID_MARKET, "51-250", 0.75)

        if has_careers_page or people_count >= 2:
            return (CompanySizeTier.SMALL_BUSINESS, "11-50", 0.65)

        return (CompanySizeTier.SOLOPRENEUR_MICRO, "1-10", 0.60)
