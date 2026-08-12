"""
Service Recommendation Engine (Phase 07).
Maps identified technical & marketing gaps to specific recommended agency services with rationales.
"""

from src.ai_insights.models import RecommendedServiceItem
from src.enrichment.models import CompanyEnrichmentReport


class ServiceRecommendationEngine:
    """Generates targeted agency service recommendations supported by enrichment evidence."""

    def generate_recommendations(self, report: CompanyEnrichmentReport) -> list[RecommendedServiceItem]:
        """
        Returns list of RecommendedServiceItem models.
        """
        recs: list[RecommendedServiceItem] = []

        # 1. Conversion Rate Optimization (CRO)
        if report.marketing_intelligence and report.marketing_intelligence.conversion.conversion_score < 60.0:
            recs.append(RecommendedServiceItem(
                service_name="Conversion Rate Optimization (CRO)",
                priority="High",
                rationale="The website lacks instant quote forms or live chat widgets, limiting visitor lead capture efficiency.",
                supporting_signals=["Conversion Score < 60", "Missing live chat / instant booking"]
            ))

        # 2. Search Engine Optimization (SEO)
        if report.seo and report.seo.data and report.seo.data.image_alt_coverage_ratio < 0.70:
            recs.append(RecommendedServiceItem(
                service_name="SEO & Metadata Audit",
                priority="High",
                rationale="Multiple missing ALT attributes and heading hierarchy gaps hinder search engine rankings.",
                supporting_signals=[f"ALT Coverage: {report.seo.data.image_alt_coverage_ratio * 100:.0f}%"]
            ))

        # 3. Content Marketing & Strategy
        if report.marketing_intelligence and not report.marketing_intelligence.content.has_blog:
            recs.append(RecommendedServiceItem(
                service_name="Content Marketing & Blogging",
                priority="Medium",
                rationale="No active blog or resource center was detected, missing organic search traffic opportunities.",
                supporting_signals=["No active blog section detected"]
            ))

        # 4. Marketing Automation & CRM Integration
        if report.marketing_intelligence and not report.marketing_intelligence.analytics_tech.has_hubspot:
            recs.append(RecommendedServiceItem(
                service_name="Marketing Automation & CRM Setup",
                priority="Medium",
                rationale="No advanced marketing automation platform (e.g. HubSpot) was detected to nurture inbound leads.",
                supporting_signals=["Missing HubSpot / Marketing Automation tag"]
            ))

        # 5. Security & Compliance Hardening
        if report.security and report.security.data and not report.security.data.has_content_security_policy:
            recs.append(RecommendedServiceItem(
                service_name="Security & Compliance Hardening",
                priority="Low",
                rationale="Website is missing Content Security Policy (CSP) header protection against cross-site scripting.",
                supporting_signals=["Security Header Score < 100", "Missing CSP header"]
            ))

        # Default fallback recommendation if website is highly optimized
        if not recs:
            recs.append(RecommendedServiceItem(
                service_name="Paid Search & Growth Campaigns (PPC)",
                priority="Medium",
                rationale="Website foundation is strong; scale customer acquisition via targeted Google Search Ads.",
                supporting_signals=["Strong baseline technical posture"]
            ))

        return recs
