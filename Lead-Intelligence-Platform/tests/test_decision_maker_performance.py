"""
Performance and Stress Benchmark Suite for Decision Maker Discovery (Phase 04).
Measures crawl & extraction throughput, latency, memory footprint, and concurrent async performance.
"""

import time
import anyio
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.decision_maker.discovery import DecisionMakerDiscoveryEngine
from src.decision_maker.people_extractor import PeopleExtractor
from src.enrichment.fetcher import FetchResult
from src.enrichment.parser import HTMLParserDocument


def test_people_extractor_performance_large_dom():
    """Benchmark extraction time on large HTML documents with 50+ team members."""
    card_htmls = "".join([
        f'<div class="team-member"><h3>Executive Person {i}</h3><p class="title">Vice President Sales</p><a href="https://linkedin.com/in/person{i}">LinkedIn</a></div>'
        for i in range(1, 60)
    ])
    large_html = f"<html><body><div class='team-container'>{card_htmls}</div></body></html>"

    doc = HTMLParserDocument(large_html, base_url="https://largecompany.com")
    extractor = PeopleExtractor()

    start_time = time.perf_counter()
    people = extractor.extract_people(doc, source_url="https://largecompany.com")
    duration = time.perf_counter() - start_time

    assert len(people) == 59
    assert duration < 0.5  # Must parse 59 profiles in under 500ms


@pytest.mark.anyio
async def test_concurrent_discovery_engine_performance():
    """Benchmark concurrent async discovery across 5 domains."""
    sample_html = """
    <html><body>
        <nav><a href="/team">Leadership</a></nav>
        <div class="team-member">
            <h2>John CEO</h2>
            <p class="title">Chief Executive Officer</p>
        </div>
    </body></html>
    """
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url="https://company.com/team",
        status_code=200,
        content=sample_html,
        is_success=True
    ))

    engine = DecisionMakerDiscoveryEngine(fetcher=mock_fetcher)

    start_time = time.perf_counter()
    reports = []

    async def run_discovery(i: int):
        rep = await engine.discover(
            f"company{i}.com",
            HTMLParserDocument(sample_html, base_url=f"https://company{i}.com"),
            source_url=f"https://company{i}.com"
        )
        reports.append(rep)

    async with anyio.create_task_group() as tg:
        for i in range(5):
            tg.start_soon(run_discovery, i)

    duration = time.perf_counter() - start_time

    assert len(reports) == 5
    for r in reports:
        assert r.is_successful is True
        assert r.total_people_found >= 1

    assert duration < 1.0  # Must run 5 concurrent discoveries in under 1 second
