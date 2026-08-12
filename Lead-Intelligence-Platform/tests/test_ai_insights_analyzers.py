"""
Unit tests for Phase 07 AI Insights sub-analyzers:
ExecutiveSummaryGenerator, DigitalMaturityAnalyzer, StrengthsWeaknessesAnalyzer, OpportunityAnalyzer, ServiceRecommendationEngine, OutreachStrategyGenerator, RiskAssessmentAnalyzer.
"""

from src.ai_insights import (
    DigitalMaturityAnalyzer,
    ExecutiveSummaryGenerator,
    OpportunityAnalyzer,
    OutreachStrategyGenerator,
    RiskAssessmentAnalyzer,
    ServiceRecommendationEngine,
    StrengthsWeaknessesAnalyzer,
)
from src.business_intelligence.models import BusinessIntelligenceReport, CompanySizeTier, IndustryCategory
from src.enrichment.models import CompanyEnrichmentReport, FetchResult, WebsiteMetadata
from src.marketing_intelligence.models import MarketingIntelligenceReport, MarketingMaturity, MarketingMaturityLevel


def _dummy_fetch(url: str = "https://example.com") -> FetchResult:
    return FetchResult(url=url, status_code=200, is_success=True)


def test_executive_summary_generator():
    gen = ExecutiveSummaryGenerator()
    report = CompanyEnrichmentReport(
        domain="roofingpro.com.au",
        fetch_result=_dummy_fetch("https://roofingpro.com.au"),
        metadata=WebsiteMetadata(title="Roofing Pro - Commercial Roofers"),
        business_intelligence=BusinessIntelligenceReport(
            domain="roofingpro.com.au",
            industry=IndustryCategory.ROOFING,
            company_size_tier=CompanySizeTier.SMALL_BUSINESS,
            estimated_employee_range="11-50"
        )
    )

    summary = gen.generate_summary(report)
    assert "roofingpro.com.au" in summary
    assert "Roofing company" in summary


def test_digital_maturity_analyzer():
    analyzer = DigitalMaturityAnalyzer()
    report = CompanyEnrichmentReport(
        domain="daikin.com.au",
        fetch_result=_dummy_fetch("https://daikin.com.au"),
        marketing_intelligence=MarketingIntelligenceReport(
            domain="daikin.com.au",
            marketing_maturity=MarketingMaturity(level=MarketingMaturityLevel.ADVANCED, score=80),
            overall_score=80
        )
    )

    maturity = analyzer.calculate_overall_maturity(report)
    assert maturity.score >= 50


def test_strengths_and_weaknesses_analyzer():
    analyzer = StrengthsWeaknessesAnalyzer()
    report = CompanyEnrichmentReport(domain="apexroofing.com", fetch_result=_dummy_fetch("https://apexroofing.com"))
    strengths, weaknesses = analyzer.analyze_strengths_and_weaknesses(report)

    assert len(strengths) >= 1
    assert len(weaknesses) >= 1


def test_service_recommendation_engine():
    engine = ServiceRecommendationEngine()
    report = CompanyEnrichmentReport(domain="testsite.com", fetch_result=_dummy_fetch("https://testsite.com"))
    recs = engine.generate_recommendations(report)

    assert len(recs) >= 1
    assert recs[0].service_name is not None


def test_outreach_strategy_generator():
    gen = OutreachStrategyGenerator()
    report = CompanyEnrichmentReport(domain="testsite.com", fetch_result=_dummy_fetch("https://testsite.com"))
    strat = gen.generate_strategy(report)

    assert strat.primary_contact_target is not None
    assert strat.opening_angle is not None
    assert len(strat.talking_points) >= 1
