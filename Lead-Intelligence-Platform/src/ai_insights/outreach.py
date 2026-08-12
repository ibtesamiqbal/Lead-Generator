"""
Outreach Strategy Generator (Phase 07).
Generates consultative outreach strategy, opening angle, target contact role, and talking points.
"""

from src.ai_insights.models import OutreachStrategy
from src.enrichment.models import CompanyEnrichmentReport


class OutreachStrategyGenerator:
    """Recommends targeted outreach hook, target executive role, and pitch talking points."""

    def generate_strategy(self, report: CompanyEnrichmentReport) -> OutreachStrategy:
        """
        Returns populated OutreachStrategy model.
        """
        strat = OutreachStrategy()

        # 1. Target Contact Role
        if report.decision_maker_discovery and report.decision_maker_discovery.decision_makers:
            top_dm = report.decision_maker_discovery.decision_makers[0]
            strat.primary_contact_target = f"{top_dm.name} ({top_dm.title})"
        elif report.business_intelligence and report.business_intelligence.industry:
            ind = report.business_intelligence.industry.value
            if ind in ("Roofing", "HVAC", "Plumbing", "Electrical"):
                strat.primary_contact_target = "Owner / General Manager"
            elif ind == "SaaS":
                strat.primary_contact_target = "VP Marketing / Chief Revenue Officer"
            else:
                strat.primary_contact_target = "Managing Director / CEO"

        # 2. Opening Angle & Hook
        industry_name = report.business_intelligence.industry.value if (report.business_intelligence and report.business_intelligence.industry) else "business"

        if report.marketing_intelligence and report.marketing_intelligence.conversion.conversion_score < 50.0:
            strat.opening_angle = f"Help {report.domain} capture 20-30% more online quote requests from existing website visitors."
            strat.suggested_tone = "Consultative & Value-Focused"
        elif report.seo and report.seo.data and report.seo.data.image_alt_coverage_ratio < 0.60:
            strat.opening_angle = f"Audit and unlock missed organic Google Search rankings for {report.domain}."
            strat.suggested_tone = "Technical & Data-Driven"
        else:
            strat.opening_angle = f"Scalable digital growth strategy to expand {industry_name} market share."
            strat.suggested_tone = "Strategic Partnership"

        # 3. Key Pitch Talking Points
        strat.talking_points = [
            f"Reference domain {report.domain} digital posture findings.",
            "Highlight specific conversion or SEO gap identified during audit.",
            "Propose quick 15-minute introductory growth strategy session."
        ]

        return strat
