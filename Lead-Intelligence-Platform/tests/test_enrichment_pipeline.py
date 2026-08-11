"""
Unit Tests for EnrichmentPipeline Orchestrator.
Integrates mock HTTPTransport with repository updates and full pipeline workflow.
"""

import pytest
import httpx
from src.database.repository import InMemoryCompanyRepository
from src.discovery.models import Company, TargetStatus
from src.enrichment.enrichment_pipeline import EnrichmentPipeline
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.models import CMSType


@pytest.mark.anyio
async def test_enrichment_pipeline_end_to_end():
    """Verify full end-to-end enrichment pipeline execution for a company target."""
    html_page = """
    <html>
      <head>
        <title>Apex Roofing Sydney</title>
        <meta name="description" content="Quality commercial and residential roofing Sydney.">
        <meta name="generator" content="WordPress 6.4">
      </head>
      <body>
        <h1>Apex Roofing Solutions</h1>
        <p>Email: <a href="mailto:info@apexroofing.com.au">info@apexroofing.com.au</a></p>
        <p>Call us: <a href="tel:0298765432">(02) 9876 5432</a></p>
        <a href="https://facebook.com/apexroofing">Facebook</a>
      </body>
    </html>
    """

    robots_content = "User-agent: *\nDisallow: /admin/\nSitemap: https://apexroofing.com.au/sitemap.xml\n"
    sitemap_content = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://apexroofing.com.au/</loc></url></urlset>'

    def handler(request):
        url_str = str(request.url)
        if "robots.txt" in url_str:
            return httpx.Response(200, text=robots_content)
        elif "sitemap.xml" in url_str:
            return httpx.Response(200, text=sitemap_content)
        else:
            return httpx.Response(200, text=html_page)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        repo = InMemoryCompanyRepository()
        company = repo.add(Company(domain="apexroofing.com.au"))

        pipeline = EnrichmentPipeline(repository=repo, fetcher=fetcher)
        report = await pipeline.enrich_company(company)

        # Assert report metadata
        assert report.is_successful is True
        assert report.metadata.title == "Apex Roofing Sydney"
        assert "info@apexroofing.com.au" in report.contacts.emails
        assert "+61298765432" in report.contacts.phone_numbers
        assert report.socials.facebook == "https://facebook.com/apexroofing"
        assert report.cms.cms_name == CMSType.WORDPRESS
        assert report.robots.is_found is True
        assert report.sitemap.is_found is True

        # Assert Phase 2 Technical & Marketing Intelligence outputs
        assert report.seo is not None
        assert report.seo.data.h1_count == 1
        assert report.structured_data is not None
        assert report.tech_stack is not None
        assert report.performance is not None
        assert report.accessibility is not None
        assert report.links is not None
        assert report.security is not None

        # Assert repository state update
        updated_company = repo.get_by_domain("apexroofing.com.au")
        assert updated_company.status == TargetStatus.ANALYZED
        assert updated_company.name.value == "Apex Roofing Sydney"
