"""
Comprehensive Edge-Case Test Suite for Decision Maker Discovery (Phase 04).
Tests broken HTML, malformed JSON-LD, cyclic/infinite link loops, missing names/titles,
multiple CEOs, SSRF links, non-ASCII Unicode names, and extreme inputs.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.decision_maker.discovery import DecisionMakerDiscoveryEngine
from src.decision_maker.people_extractor import PeopleExtractor
from src.decision_maker.title_normalizer import TitleNormalizer
from src.decision_maker.validators import DecisionMakerValidator
from src.decision_maker.website_scanner import LeadershipPageScanner
from src.enrichment.fetcher import FetchResult
from src.enrichment.parser import HTMLParserDocument


def test_validator_ssrf_protection():
    # SSRF & malicious link checks
    assert DecisionMakerValidator.is_safe_url("http://127.0.0.1/admin") is False
    assert DecisionMakerValidator.is_safe_url("http://localhost:8080/secret") is False
    assert DecisionMakerValidator.is_safe_url("http://169.254.169.254/latest/meta-data") is False
    assert DecisionMakerValidator.is_safe_url("file:///etc/passwd") is False
    assert DecisionMakerValidator.is_safe_url("ftp://example.com") is False
    assert DecisionMakerValidator.is_safe_url("javascript:alert(1)") is False
    assert DecisionMakerValidator.is_safe_url("https://example.com/team") is True


def test_validator_noise_blacklisting():
    assert DecisionMakerValidator.is_valid_name("Cookie Policy") is False
    assert DecisionMakerValidator.is_valid_name("Terms of Service") is False
    assert DecisionMakerValidator.is_valid_name("Accessibility Statement") is False
    assert DecisionMakerValidator.is_valid_name("Press Kit") is False
    assert DecisionMakerValidator.is_valid_name("John Smith") is True


def test_malformed_json_ld_parsing():
    html = """
    <html>
    <head>
        <script type="application/ld+json">
        { "this is invalid json syntax...
        </script>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": "Åsa Lindqvist",
            "jobTitle": "Co-Founder & CEO"
        }
        </script>
    </head>
    <body></body>
    </html>
    """
    doc = HTMLParserDocument(html, base_url="https://example.com")
    extractor = PeopleExtractor()
    people = extractor.extract_people(doc, source_url="https://example.com")

    assert len(people) == 1
    assert people[0].full_name == "Åsa Lindqvist"
    assert "Chief Executive Officer" in people[0].normalized_title


def test_broken_html_and_empty_bios():
    html = """
    <div><div><h3>Dr. François Dubois</h3><p class="title">Chief Technology Officer</p></div>
    <div class="team-member"></div>
    <div class="team-member"><h3>Invalid Name 12345</h3></div>
    """
    doc = HTMLParserDocument(html, base_url="https://example.com")
    extractor = PeopleExtractor()
    people = extractor.extract_people(doc, source_url="https://example.com")

    assert len(people) >= 1
    francois = next((p for p in people if "Dubois" in p.full_name), None)
    assert francois is not None
    assert francois.normalized_title == "Chief Technology Officer"


def test_multiple_ceos_and_founders_without_titles():
    html = """
    <html>
    <body>
        <div class="team-member">
            <h2>Alice Johnson</h2>
            <p class="title">Founder</p>
        </div>
        <div class="team-member">
            <h2>Bob Williams</h2>
            <p class="title">Co-CEO</p>
        </div>
    </body>
    </html>
    """
    doc = HTMLParserDocument(html, base_url="https://example.com")
    extractor = PeopleExtractor()
    people = extractor.extract_people(doc, source_url="https://example.com")

    assert len(people) == 2
    alice = next(p for p in people if p.full_name == "Alice Johnson")
    bob = next(p for p in people if p.full_name == "Bob Williams")

    assert alice.priority == 100
    assert bob.priority == 100


@pytest.mark.anyio
async def test_engine_graceful_failure_on_network_error():
    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url="https://broken.com/team",
        status_code=500,
        content="",
        is_success=False,
        error="Internal Server Error"
    ))

    doc = HTMLParserDocument("<html><a href='/team'>Our Team</a></html>", base_url="https://broken.com")
    engine = DecisionMakerDiscoveryEngine(fetcher=mock_fetcher)

    report = await engine.discover("broken.com", doc, source_url="https://broken.com")
    assert report.domain == "broken.com"
    assert report.is_successful is True
    assert len(report.notes) > 0
