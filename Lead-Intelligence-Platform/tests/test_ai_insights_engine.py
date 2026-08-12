"""
Integration tests for Phase 07 AI Insights Engine and Enrichment Pipeline integration across multiple industries.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.ai_insights import AIInsightsEngine
from src.discovery.models import Company, MetadataField
from src.enrichment.enrichment_pipeline import EnrichmentPipeline
from src.enrichment.fetcher import FetchResult
from src.enrichment.models import CompanyEnrichmentReport, WebsiteMetadata


@pytest.mark.anyio
async def test_ai_insights_engine_end_to_end():
    report_in = CompanyEnrichmentReport(
        domain="hubspot.com",
        metadata=WebsiteMetadata(title="HubSpot - Software"),
        fetch_result=FetchResult(url="https://hubspot.com", status_code=200, is_success=True)
    )

    engine = AIInsightsEngine()
    ai_report = await engine.analyze(report_in)

    assert ai_report.domain == "hubspot.com"
    assert "hubspot.com" in ai_report.executive_summary
    assert ai_report.digital_maturity.score >= 0
    assert len(ai_report.strengths) >= 1
    assert len(ai_report.weaknesses) >= 1
    assert len(ai_report.recommended_services) >= 1
    assert ai_report.outreach_strategy.opening_angle is not None


@pytest.mark.anyio
@pytest.mark.parametrize("industry_keyword, domain_name", [
    ("Roofing", "roofingpro.com.au"),
    ("HVAC", "daikin.com.au"),
    ("SaaS", "hubspot.com"),
    ("Law Firm", "legalpartners.com.au"),
    ("Marketing Agency", "growthagency.io")
])
async def test_multi_industry_pipeline_integration(industry_keyword: str, domain_name: str):
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url=f"https://{domain_name}",
        status_code=200,
        content=f"<html><head><title>{domain_name} - Top {industry_keyword} Services</title></head><body><h1>{industry_keyword} Experts</h1><a href='/contact'>Contact Us</a></body></html>",
        is_success=True
    ))

    pipeline = EnrichmentPipeline(fetcher=mock_fetcher)
    report = await pipeline.enrich_domain(domain_name)

    assert report.domain == domain_name
    assert hasattr(report, "ai_insights")
    assert report.ai_insights is not None
    assert report.ai_insights.confidence >= 0.60
    assert len(report.ai_insights.recommended_services) >= 1
