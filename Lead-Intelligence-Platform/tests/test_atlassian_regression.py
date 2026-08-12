"""
Permanent Regression Test Suite for Atlassian Extraction (Phase 04).
Ensures marketing headlines ("For insights that matter..."), CTAs, and product pages
(/project-management, /team-playbook) are NEVER extracted or misclassified as Decision Makers or Leadership Pages.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.decision_maker.discovery import DecisionMakerDiscoveryEngine
from src.decision_maker.people_extractor import PeopleExtractor
from src.decision_maker.validators import DecisionMakerValidator
from src.decision_maker.website_scanner import LeadershipPageScanner
from src.enrichment.fetcher import FetchResult
from src.enrichment.parser import HTMLParserDocument


def test_atlassian_marketing_headline_rejected():
    marketing_headline = "For insights that matter - Partner With Rovo To Update Your Strategy, Specs, and Tasks Based On the Latest Meeting."

    # Must be rejected by DecisionMakerValidator
    assert DecisionMakerValidator.is_valid_name(marketing_headline) is False


def test_atlassian_non_leadership_pages_rejected():
    scanner = LeadershipPageScanner()
    doc = HTMLParserDocument("<html></html>", base_url="https://www.atlassian.com")

    # Reject /project-management, /work-management/project-collaboration, /team-playbook
    p1 = scanner._evaluate_candidate_link("/project-management", "Project Management", "https://www.atlassian.com", "www.atlassian.com", "Navigation Menu")
    p2 = scanner._evaluate_candidate_link("/work-management/project-collaboration", "Project Collaboration", "https://www.atlassian.com", "www.atlassian.com", "Navigation Menu")
    p3 = scanner._evaluate_candidate_link("/team-playbook", "Team Playbook", "https://www.atlassian.com", "www.atlassian.com", "Navigation Menu")

    assert p1 is None
    assert p2 is None
    assert p3 is None


@pytest.mark.anyio
async def test_atlassian_end_to_end_regression():
    html_with_marketing_headline = """
    <html>
    <body>
        <nav>
            <a href="/project-management">Project Management</a>
            <a href="/team-playbook">Team Playbook</a>
        </nav>
        <div class="card">
            <h3>For insights that matter - Partner With Rovo To Update Your Strategy</h3>
            <p class="title">Executive</p>
        </div>
    </body>
    </html>
    """
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url="https://www.atlassian.com/project-management",
        status_code=200,
        content=html_with_marketing_headline,
        is_success=True
    ))

    doc = HTMLParserDocument(html_with_marketing_headline, base_url="https://www.atlassian.com")
    engine = DecisionMakerDiscoveryEngine(fetcher=mock_fetcher)

    report = await engine.discover("atlassian.com", doc, source_url="https://www.atlassian.com")

    assert report.domain == "atlassian.com"
    # Must report 0 verified decision makers and 0 non-leadership pages
    assert report.total_people_found == 0
    assert len(report.decision_makers) == 0
    assert len(report.leadership_pages) == 0
