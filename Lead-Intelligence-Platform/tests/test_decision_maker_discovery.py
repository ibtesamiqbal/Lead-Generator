"""
Unit tests for end-to-end DecisionMakerDiscoveryEngine async pipeline.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.decision_maker.discovery import DecisionMakerDiscoveryEngine
from src.enrichment.fetcher import FetchResult
from src.enrichment.parser import HTMLParserDocument


@pytest.mark.anyio
async def test_decision_maker_discovery_engine():
    primary_html = """
    <html>
    <body>
        <nav><a href="/team">Leadership Team</a></nav>
        <div class="team-member">
            <h2>Mark Davis</h2>
            <p class="title">CEO & Founder</p>
        </div>
    </body>
    </html>
    """
    team_html = """
    <html>
    <body>
        <div class="team-member">
            <h2>Mark Davis</h2>
            <p class="title">CEO & Founder</p>
            <p class="bio">Mark is the founder and CEO driving vision.</p>
        </div>
        <div class="team-member">
            <h2>Elena Rostova</h2>
            <p class="title">Head of Sales</p>
            <a href="https://linkedin.com/in/elena-rostova">LinkedIn</a>
        </div>
    </body>
    </html>
    """

    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url="https://example.com/team",
        status_code=200,
        content=team_html,
        is_success=True
    ))

    engine = DecisionMakerDiscoveryEngine(fetcher=mock_fetcher)
    doc = HTMLParserDocument(primary_html, base_url="https://example.com")

    report = await engine.discover(
        domain="example.com",
        doc=doc,
        source_url="https://example.com",
        contact_emails=["elena.rostova@example.com"]
    )

    assert report.domain == "example.com"
    assert report.total_people_found == 2
    assert report.is_successful is True

    # Mark Davis should be top priority (100)
    top = report.decision_makers[0]
    assert top.full_name == "Mark Davis"
    assert top.priority == 100
    assert "Chief Executive Officer" in top.normalized_title

    # Elena Rostova should have Priority 70 and enriched email
    elena = next(p for p in report.decision_makers if p.full_name == "Elena Rostova")
    assert elena.priority == 70
    assert elena.email == "elena.rostova@example.com"
    assert elena.linkedin_url == "https://linkedin.com/in/elena-rostova"
