"""
Risk Assessment Analyzer (Phase 07).
Identifies uncertain signals, missing pages, or low-confidence estimates.
"""

from src.enrichment.models import CompanyEnrichmentReport


class RiskAssessmentAnalyzer:
    """Highlights risk factors, missing data points, or confidence caveats."""

    def assess_risks(self, report: CompanyEnrichmentReport) -> list[str]:
        """
        Returns list of risk caveat strings.
        """
        risks: list[str] = []

        if report.business_intelligence and report.business_intelligence.company_size_confidence:
            if report.business_intelligence.company_size_confidence < 0.70:
                risks.append("Estimated company employee size has medium/low confidence due to limited public team data.")

        if report.decision_maker_discovery and report.decision_maker_discovery.total_people_found == 0:
            risks.append("No public leadership or management pages found; executive contact research required.")

        if report.contacts and not report.contacts.emails:
            risks.append("No direct public email addresses discovered on website DOM.")

        if not report.fetch_result or not report.fetch_result.is_success:
            risks.append("Website response returned non-200 status or network failure.")

        return risks
