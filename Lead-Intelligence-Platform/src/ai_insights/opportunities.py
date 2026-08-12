"""
Opportunity Analyzer (Phase 07).
Categorizes opportunities across SEO, Marketing, Conversion, and Sales enablements.
"""

from src.ai_insights.models import OpportunityBreakdown
from src.enrichment.models import CompanyEnrichmentReport


class OpportunityAnalyzer:
    """Extracts high-impact digital opportunities across four core pillars."""

    def analyze_opportunities(self, report: CompanyEnrichmentReport) -> OpportunityBreakdown:
        """
        Returns populated OpportunityBreakdown model.
        """
        opps = OpportunityBreakdown()

        # 1. SEO Opportunities
        if report.seo and report.seo.data:
            d = report.seo.data
            if not d.heading_structure_valid:
                opps.seo.append("Fix H1 heading hierarchy for primary keywords")
            if d.image_alt_coverage_ratio < 0.80:
                opps.seo.append("Add ALT text attributes to missing images to improve image search SEO")
            if d.internal_links_count < 10:
                opps.seo.append("Expand internal cross-linking between service pages")
        if report.sitemap and not report.sitemap.is_found:
            opps.seo.append("Generate and submit an XML sitemap to Google Search Console")

        # 2. Marketing Opportunities
        if report.marketing_intelligence:
            mi = report.marketing_intelligence
            if not mi.content.has_blog:
                opps.marketing.append("Publish regular educational blog articles to attract organic search traffic")
            if not mi.content.has_case_studies:
                opps.marketing.append("Publish customer case studies and proof-of-work project stories")
            if mi.social and mi.social.social_completeness_score < 75.0:
                opps.marketing.append("Claim and link missing social media profiles (LinkedIn, YouTube)")

        # 3. Conversion Opportunities
        if report.marketing_intelligence and report.marketing_intelligence.conversion:
            c = report.marketing_intelligence.conversion
            if not c.has_quote_request and not c.has_demo_request:
                opps.conversion.append("Add high-visibility 'Request a Free Quote' form to header/hero section")
            if not c.has_live_chat:
                opps.conversion.append("Implement live chat or AI chat agent for instant visitor lead capture")
            if not c.has_booking_system:
                opps.conversion.append("Integrate automated appointment scheduling (e.g. Calendly / HubSpot Meetings)")

        # 4. Sales Enablement Opportunities
        if report.decision_maker_discovery and report.decision_maker_discovery.total_people_found > 0:
            opps.sales.append(f"Direct outreach to {report.decision_maker_discovery.total_people_found} identified key executives")
        else:
            opps.sales.append("Conduct targeted LinkedIn Sales Navigator research to find decision maker emails")

        if report.business_intelligence and report.business_intelligence.hiring and report.business_intelligence.hiring.currently_hiring:
            opps.sales.append("Target active hiring growth with tailored agency pitch")

        return opps
