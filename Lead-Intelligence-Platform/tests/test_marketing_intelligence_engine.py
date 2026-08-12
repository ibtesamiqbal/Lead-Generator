"""
Integration tests for Phase 06 Marketing Intelligence Engine and Enrichment Pipeline integration.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.discovery.models import Company, MetadataField
from src.enrichment.enrichment_pipeline import EnrichmentPipeline
from src.enrichment.fetcher import FetchResult
from src.enrichment.models import WebsiteMetadata
from src.enrichment.parser import HTMLParserDocument
from src.marketing_intelligence import MarketingIntelligenceEngine, MarketingMaturityLevel


@pytest.mark.anyio
async def test_marketing_intelligence_engine_end_to_end():
    sample_html = """
    <html>
    <head><title>HubSpot - CRM & Marketing Automation</title></head>
    <body>
        <h1>Grow Better With HubSpot</h1>
        <a href="/demo" class="btn">Schedule a Demo</a>
        <a href="/blog">Our Blog</a>
        <p>Read case studies and customer stories.</p>
        <script src="https://js.intercomcdn.com/intercom.js"></script>
    </body>
    </html>
    """
    doc = HTMLParserDocument(sample_html, base_url="https://hubspot.com")
    metadata = WebsiteMetadata(title="HubSpot CRM", meta_description="Marketing software")
    engine = MarketingIntelligenceEngine()

    report = await engine.analyze(
        domain="hubspot.com",
        doc=doc,
        metadata=metadata,
        source_url="https://hubspot.com"
    )

    assert report.domain == "hubspot.com"
    assert report.content.has_blog is True
    assert report.content.has_case_studies is True
    assert report.conversion.has_demo_request is True
    assert report.conversion.has_live_chat is True
    assert report.cta.primary_cta is not None
    assert report.overall_score >= 40


@pytest.mark.anyio
async def test_pipeline_integration_with_phase_06():
    mock_company = Company(domain="hubspot.com", name=MetadataField[str](value="HubSpot", confidence=1.0, source="test"))

    sample_html = "<html><head><title>HubSpot</title></head><body><a href='/demo' class='btn'>Get a Demo</a></body></html>"
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url="https://hubspot.com",
        status_code=200,
        content=sample_html,
        is_success=True
    ))

    pipeline = EnrichmentPipeline(fetcher=mock_fetcher)
    report = await pipeline.enrich_domain("hubspot.com")

    assert report.domain == "hubspot.com"
    assert hasattr(report, "marketing_intelligence")
    assert report.marketing_intelligence is not None
    assert report.marketing_intelligence.overall_score >= 0
