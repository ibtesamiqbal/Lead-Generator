"""
Integration, Multi-Industry, and Batch Performance Benchmark tests for Phase 08 Lead Scoring Engine.
"""

import time
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.enrichment.enrichment_pipeline import EnrichmentPipeline
from src.enrichment.fetcher import FetchResult
from src.enrichment.models import CompanyEnrichmentReport
from src.lead_scoring import LeadScoringEngine


def _dummy_fetch(url: str = "https://example.com") -> FetchResult:
    return FetchResult(url=url, status_code=200, is_success=True)


@pytest.mark.anyio
async def test_lead_scoring_engine_end_to_end():
    report_in = CompanyEnrichmentReport(domain="hubspot.com", fetch_result=_dummy_fetch("https://hubspot.com"))
    engine = LeadScoringEngine()
    scoring_report = await engine.analyze(report_in)

    assert scoring_report.domain == "hubspot.com"
    assert 0 <= scoring_report.overall_score <= 100
    assert scoring_report.grade is not None
    assert scoring_report.priority is not None


@pytest.mark.anyio
@pytest.mark.parametrize("domain_name", [
    "roofingpro.com.au",
    "daikin.com.au",
    "hubspot.com",
    "legalpartners.com.au",
    "growthagency.io"
])
async def test_multi_industry_lead_scoring_pipeline(domain_name: str):
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url=f"https://{domain_name}",
        status_code=200,
        content=f"<html><head><title>{domain_name}</title></head><body><h1>Services</h1></body></html>",
        is_success=True
    ))

    pipeline = EnrichmentPipeline(fetcher=mock_fetcher)
    report = await pipeline.enrich_domain(domain_name)

    assert report.domain == domain_name
    assert hasattr(report, "lead_scoring")
    assert report.lead_scoring is not None
    assert 0 <= report.lead_scoring.overall_score <= 100
    assert len(report.lead_scoring.reason_codes) >= 1


def test_batch_performance_benchmark_10k_simulated_domains():
    """
    Performance Benchmark Test:
    Ensures LeadScoringEngine processes 10,000+ domain scoring calls in < 1.0 second (< 0.1ms per domain).
    """
    report_in = CompanyEnrichmentReport(domain="benchmark.com", fetch_result=_dummy_fetch("https://benchmark.com"))
    engine = LeadScoringEngine()

    start_time = time.perf_counter()
    for _ in range(10000):
        engine.scoring_engine.score_report(report_in)
    duration = time.perf_counter() - start_time

    per_domain_ms = (duration / 10000.0) * 1000.0
    assert duration < 1.0, f"Batch 10,000 scoring took {duration:.3f}s (target < 1.0s)"
    assert per_domain_ms < 0.1, f"Per domain scoring took {per_domain_ms:.4f}ms (target < 0.1ms)"
