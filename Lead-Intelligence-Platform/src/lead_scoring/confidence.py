"""
Confidence Engine (Phase 08).
Calculates data completeness, signal agreement, and overall lead scoring confidence score.
"""

from src.enrichment.models import CompanyEnrichmentReport
from src.lead_scoring.validators import LeadScoringValidator


class ConfidenceEngine:
    """Evaluates data completeness ratio and decision-maker verification ratio."""

    def calculate_confidence(self, report: CompanyEnrichmentReport) -> float:
        """
        Returns normalized float confidence score in [0.0, 1.0].
        """
        pts = 0.0

        # Fetch status
        if report.fetch_result and report.fetch_result.is_success: pts += 0.25

        # Decision maker discovery
        if report.decision_maker_discovery:
            dm_count = report.decision_maker_discovery.total_people_found
            if dm_count >= 1: pts += 0.30

        # Public contacts
        if report.contacts and report.contacts.emails: pts += 0.15
        if report.contacts and report.contacts.phone_numbers: pts += 0.10

        # Business & Marketing intelligence
        if report.business_intelligence: pts += 0.10
        if report.marketing_intelligence: pts += 0.10

        return LeadScoringValidator.clamp_confidence(pts)
