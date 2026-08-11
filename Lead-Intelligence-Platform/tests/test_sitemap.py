"""
Unit Tests for SitemapParser.
Mocks XML sitemap responses using httpx.MockTransport.
"""

import pytest
import httpx
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.sitemap import SitemapParser


@pytest.mark.anyio
async def test_sitemap_xml_parsing():
    """Verify XML sitemap URL extraction."""
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://roofingpro.com.au/</loc></url>
      <url><loc>https://roofingpro.com.au/about</loc></url>
      <url><loc>https://roofingpro.com.au/contact</loc></url>
    </urlset>
    """

    def handler(request):
        return httpx.Response(200, text=sitemap_xml)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        parser = SitemapParser(fetcher=fetcher)
        data = await parser.fetch_and_parse("https://roofingpro.com.au")

        assert data.is_found is True
        assert data.url_count == 3
        assert "https://roofingpro.com.au/about" in data.sitemap_urls


@pytest.mark.anyio
async def test_sitemap_xml_invalid_syntax():
    """Verify graceful error handling for invalid XML."""
    def handler(request):
        return httpx.Response(200, text="<invalid xml file format")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        parser = SitemapParser(fetcher=fetcher)
        data = await parser.fetch_and_parse("https://roofingpro.com.au")

        assert data.is_found is False
        assert data.url_count == 0
