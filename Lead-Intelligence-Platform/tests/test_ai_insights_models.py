"""
Unit tests for Phase 07 — AI Insights & Opportunity Analysis Data Models.
"""

from src.ai_insights.models import (
    AIInsightsReport,
    DigitalMaturityTier,
    OpportunityBreakdown,
    OverallDigitalMaturity,
    OutreachStrategy,
    RecommendedServiceItem,
)


def test_ai_insights_report_instantiation():
    report = AIInsightsReport(
        domain="daikin.com.au",
        executive_summary="daikin.com.au is a leading HVAC manufacturer and distributor in Australia.",
        digital_maturity=OverallDigitalMaturity(level=DigitalMaturityTier.ADVANCED, score=85, confidence=0.92),
        strengths=["Strong brand recognition", "Fast website performance"],
        weaknesses=["Missing CSP security header", "Low image ALT coverage"],
        opportunities=OpportunityBreakdown(seo=["Add ALT text to 25 images"], marketing=["Publish HVAC whitepapers"]),
        recommended_services=[RecommendedServiceItem(service_name="SEO Optimization", priority="High", rationale="Fix ALT coverage")],
        outreach_strategy=OutreachStrategy(primary_contact_target="Managing Director", opening_angle="Unlock 20% growth"),
        risks=["Employee count estimation has medium confidence"],
        confidence=0.90
    )

    assert report.domain == "daikin.com.au"
    assert report.digital_maturity.level == DigitalMaturityTier.ADVANCED
    assert len(report.strengths) == 2
    assert report.recommended_services[0].service_name == "SEO Optimization"
    assert report.confidence == 0.90
