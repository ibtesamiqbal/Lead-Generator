"""
Unit Tests for AddressFinder.
"""

from src.contact_discovery.address_finder import AddressFinder
from src.enrichment.parser import HTMLParserDocument


def test_address_finder():
    """Verify physical street address, suburb, state, and postcode parsing."""
    html = """
    <html>
      <body>
        <address>100 Pitt Street, Sydney NSW 2000</address>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    finder = AddressFinder()
    addresses = finder.find_addresses(doc, source_url="https://example.com")

    assert len(addresses) >= 1
    assert "Sydney" in addresses[0].city or "Sydney" in addresses[0].raw_address
    assert addresses[0].state == "NSW"
    assert addresses[0].postal_code == "2000"
