"""
Unit Tests for RobotsTxtParser.
Mocks HTTP response via httpx.MockTransport.
"""

import pytest
import httpx
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.robots import RobotsTxtParser


@pytest.mark.anyio
async def test_robots_txt_parsing():
    """Verify parsing of user-agent rules and sitemap directives from robots.txt."""
    robots_content = """
    User-agent: *
    Disallow: /admin/
    Disallow: /private/
    Allow: /public/
    
    Sitemap: https://roofingpro.com.au/sitemap.xml
    Sitemap: https://roofingpro.com.au/sitemap_news.xml
    """

    def handler(request):
        return httpx.Response(200, text=robots_content)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        parser = RobotsTxtParser(fetcher=fetcher)
        data = await parser.fetch_and_parse("https://roofingpro.com.au")

        assert data.is_found is True
        assert len(data.rules) == 3
        assert data.sitemap_urls == [
            "https://roofingpro.com.au/sitemap.xml",
            "https://roofingpro.com.au/sitemap_news.xml"
        ]


@pytest.mark.anyio
async def test_robots_txt_not_found():
    """Verify handling when robots.txt returns 404 Not Found."""
    def handler(request):
        return httpx.Response(404, text="Not Found")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        parser = RobotsTxtParser(fetcher=fetcher)
        data = await parser.fetch_and_parse("https://roofingpro.com.au")

        assert data.is_found is False
        assert len(data.rules) == 0
        assert len(data.sitemap_urls) == 0
