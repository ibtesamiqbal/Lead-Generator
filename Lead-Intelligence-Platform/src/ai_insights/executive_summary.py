"""
Executive Summary Generator (Phase 07).
Generates concise multi-sentence business summary using structured phase data.
"""

from src.enrichment.models import CompanyEnrichmentReport


class ExecutiveSummaryGenerator:
    """Synthesizes structured business summary without external LLM API calls."""

    def generate_summary(self, report: CompanyEnrichmentReport) -> str:
        """
        Builds explainable executive summary string.
        """
        domain = report.domain
        title = (report.metadata.title if report.metadata else "") or domain

        # Industry
        industry_str = "commercial business"
        if report.business_intelligence and report.business_intelligence.industry:
            industry_str = f"{report.business_intelligence.industry.value} company"

        # Company Size
        size_str = "operating in Australia"
        if report.business_intelligence and report.business_intelligence.company_size_tier:
            size_str = f"operating as a {report.business_intelligence.company_size_tier.value} ({report.business_intelligence.estimated_employee_range} employees)"

        # Marketing maturity
        maturity_str = "moderate digital presence"
        if report.marketing_intelligence:
            maturity_str = f"{report.marketing_intelligence.marketing_maturity.level.value.lower()} digital maturity (score: {report.marketing_intelligence.overall_score}/100)"

        # Tech stack / CMS snippet
        cms_str = ""
        if report.cms and hasattr(report.cms, "cms_name"):
            cms_val = report.cms.cms_name.value if hasattr(report.cms.cms_name, "value") else str(report.cms.cms_name)
            if cms_val.lower() != "unknown":
                cms_str = f" built on {cms_val}"

        # Decision Makers snippet
        dm_count = 0
        if report.decision_maker_discovery:
            dm_count = report.decision_maker_discovery.total_people_found

        dm_str = f" with {dm_count} verified decision makers identified" if dm_count > 0 else " with public leadership contact details yet to be verified"

        return f"{domain} is an established {industry_str} {size_str}{cms_str}. The company currently exhibits {maturity_str}{dm_str}."
