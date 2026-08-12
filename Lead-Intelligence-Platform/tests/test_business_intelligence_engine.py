"""
Integration tests for Phase 05 Business Intelligence Engine and Enrichment Pipeline integration.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.business_intelligence import BusinessIntelligenceEngine, IndustryCategory
from src.discovery.models import Company, MetadataField
from src.enrichment.enrichment_pipeline import EnrichmentPipeline
from src.enrichment.fetcher import FetchResult
from src.enrichment.models import WebsiteMetadata
from src.enrichment.parser import HTMLParserDocument


@pytest.mark.anyio
async def test_business_intelligence_engine_end_to_end():
    sample_html = """
    <html>
    <head><title>Apex Roofing & Solar - Commercial & Residential Roofers</title></head>
    <body>
        <h1>Apex Roofing Specialists</h1>
        <p>Founded in 2010. Serving Dallas and Fort Worth with top quality roof replacement and gutter repair.</p>
        <p>Read customer testimonials and check financing options.</p>
        <a href="/careers">Join Our Team - We're Hiring</a>
    </body>
    </html>
    """
    doc = HTMLParserDocument(sample_html, base_url="https://apexroofing.com")
    metadata = WebsiteMetadata(title="Apex Roofing & Solar")
    engine = BusinessIntelligenceEngine()

    report = await engine.analyze(
        domain="apexroofing.com",
        doc=doc,
        metadata=metadata,
        source_url="https://apexroofing.com"
    )

    assert report.domain == "apexroofing.com"
    assert report.industry == IndustryCategory.ROOFING
    assert report.founded_year == 2010
    assert report.years_in_business == 16
    assert report.trust_signals.has_testimonials is True
    assert report.trust_signals.has_financing is True
    assert report.hiring.currently_hiring is True
    assert report.hiring.has_careers_page is True


@pytest.mark.anyio
async def test_pipeline_integration_with_phase_05():
    mock_company = Company(domain="apexroofing.com", name=MetadataField[str](value="Apex Roofing", confidence=1.0, source="test"))

    sample_html = "<html><head><title>Apex Roofing</title></head><body><h1>Commercial Roofing Repair</h1></body></html>"
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url="https://apexroofing.com",
        status_code=200,
        content=sample_html,
        is_success=True
    ))

    pipeline = EnrichmentPipeline(fetcher=mock_fetcher)
    report = await pipeline.enrich_domain("apexroofing.com")

    assert report.domain == "apexroofing.com"
    assert hasattr(report, "business_intelligence")
    assert report.business_intelligence is not None
    assert report.business_intelligence.industry == IndustryCategory.ROOFING
