"""
Unit Tests for ContactPageFinder.
"""

from src.contact_discovery.models import ContactPageCategory
from src.contact_discovery.page_finder import ContactPageFinder
from src.enrichment.parser import HTMLParserDocument


def test_contact_page_finder():
    """Verify secondary contact, team, about, careers, and quote URL classification."""
    html = """
    <html>
      <body>
        <a href="https://example.com/contact-us">Contact Us</a>
        <a href="https://example.com/about-us">About Our Team</a>
        <a href="https://example.com/careers">Join Our Team</a>
        <a href="https://example.com/get-a-quote">Get A Free Quote</a>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    finder = ContactPageFinder()
    pages = finder.find_contact_pages(doc, base_url="https://example.com")

    categories = {p.url: p.category for p in pages}

    assert categories["https://example.com/contact-us"] == ContactPageCategory.CONTACT
    assert categories["https://example.com/about-us"] == ContactPageCategory.ABOUT
    assert categories["https://example.com/careers"] == ContactPageCategory.CAREERS
    assert categories["https://example.com/get-a-quote"] == ContactPageCategory.QUOTE
