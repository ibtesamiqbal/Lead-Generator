"""
Unit Tests for ContactDiscoveryEngine.
Mocks secondary contact page HTTP transport.
"""

import pytest
import httpx
from src.contact_discovery.discovery_engine import ContactDiscoveryEngine
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.parser import HTMLParserDocument


@pytest.mark.anyio
async def test_contact_discovery_engine_end_to_end():
    """Verify end-to-end ContactDiscoveryEngine workflow including secondary contact page crawling."""
    primary_html = """
    <html>
      <body>
        <p>Main Email: info@apexroofing.com.au</p>
        <a href="https://apexroofing.com.au/contact">Contact Us Page</a>
      </body>
    </html>
    """
    sec_html = """
    <html>
      <body>
        <p>Sales Email: sales@apexroofing.com.au</p>
        <p>Office Phone: (02) 9876 5432</p>
        <address>123 Pitt Street, Sydney NSW 2000</address>
      </body>
    </html>
    """

    def handler(request):
        if "contact" in str(request.url):
            return httpx.Response(200, text=sec_html)
        return httpx.Response(200, text=primary_html)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        engine = ContactDiscoveryEngine(fetcher=fetcher)

        doc = HTMLParserDocument(primary_html, base_url="https://apexroofing.com.au")
        report = await engine.discover("apexroofing.com.au", doc, source_url="https://apexroofing.com.au")

        addrs = [e.address for e in report.emails]
        assert report.is_successful is True
        assert "info@apexroofing.com.au" in addrs
        assert "sales@apexroofing.com.au" in addrs
        assert len(report.phones) >= 1
        assert "+61298765432" in [p.e164_number for p in report.phones if p.e164_number]
