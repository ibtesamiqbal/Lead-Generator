"""
Unit tests for Phase 06 — Marketing Intelligence Data Models.
"""

from src.marketing_intelligence.models import (
    ConversionOptimization,
    CTAAnalysis,
    MarketingAnalyticsTech,
    MarketingIntelligenceReport,
    MarketingMaturity,
    MarketingMaturityLevel,
    SEOIntelligenceSummary,
    SocialPresence,
)


def test_marketing_intelligence_report_instantiation():
    report = MarketingIntelligenceReport(
        domain="hubspot.com",
        marketing_maturity=MarketingMaturity(level=MarketingMaturityLevel.ADVANCED, score=82, confidence=0.90),
        seo_summary=SEOIntelligenceSummary(has_title_tag=True, title_quality="Good", has_meta_description=True, has_sitemap=True),
        social=SocialPresence(has_linkedin=True, has_facebook=True, social_completeness_score=50.0),
        conversion=ConversionOptimization(has_contact_form=True, has_demo_request=True, conversion_score=70.0),
        cta=CTAAnalysis(primary_cta="Request a Demo", total_ctas_found=5),
        analytics_tech=MarketingAnalyticsTech(has_ga4=True, has_hubspot=True, detected_marketing_tools=["GA4", "HubSpot"]),
        overall_score=82
    )

    assert report.domain == "hubspot.com"
    assert report.marketing_maturity.level == MarketingMaturityLevel.ADVANCED
    assert report.overall_score == 82
    assert report.cta.primary_cta == "Request a Demo"
    assert report.conversion.has_demo_request is True
    assert "HubSpot" in report.analytics_tech.detected_marketing_tools
