"""
CLI Integration Test for Phase 04 — Decision Maker Discovery rendering.
Verifies that `cmd_enrich_domain` cleanly formats and outputs Leadership Pages and Decision Makers.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from rich.console import Console

from src.cli import cmd_enrich_domain
from src.decision_maker.models import DecisionMaker, DecisionMakerDiscoveryReport, Department, LeadershipPage, Seniority
from src.discovery.models import Company, MetadataField, TargetStatus
from src.enrichment.models import CompanyEnrichmentReport, FetchResult, WebsiteMetadata


def test_cli_enrich_renders_decision_maker_section(capsys):
    mock_company = Company(domain="techcorp.com", name=MetadataField[str](value="TechCorp", confidence=1.0, source="test"))
    
    mock_report = CompanyEnrichmentReport(
        domain="techcorp.com",
        fetch_result=FetchResult(url="https://techcorp.com", status_code=200, content="<html></html>", is_success=True),
        metadata=WebsiteMetadata(title="TechCorp Home"),
        decision_maker_discovery=DecisionMakerDiscoveryReport(
            domain="techcorp.com",
            leadership_pages=[
                LeadershipPage(url="https://techcorp.com/team", title="Team Page", confidence=0.9, source="Navigation Menu")
            ],
            decision_makers=[
                DecisionMaker(
                    full_name="Sarah Connor",
                    title="CEO & Founder",
                    normalized_title="Chief Executive Officer",
                    department=Department.EXECUTIVE,
                    seniority=Seniority.EXECUTIVE,
                    priority=100,
                    confidence=0.95,
                    email="sarah@techcorp.com",
                    linkedin_url="https://linkedin.com/in/sarahconnor",
                    source_url="https://techcorp.com/team"
                )
            ],
            total_people_found=1
        )
    )

    with patch("src.database.repository.SQLiteCompanyRepository.get_by_domain", return_value=mock_company), \
         patch("src.enrichment.enrichment_pipeline.EnrichmentPipeline.enrich_company", return_value=mock_report):

        cmd_enrich_domain("techcorp.com")

        # Capture rich console output
        output = capsys.readouterr().out

        assert "Decision Maker Discovery (Phase 04)" in output
        assert "Leadership Pages Discovered: 1" in output
        assert "https://techcorp.com/team" in output
        assert "Sarah Connor" in output
        assert "Chief Executive Officer" in output
        assert "Executive" in output
        assert "Priority: 100" in output
        assert "Confidence: 95%" in output
        assert "sarah@techcorp.com" in output
