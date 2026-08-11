"""
Unit Tests for ContactExtractor.
"""

from src.enrichment.contact_extractor import ContactExtractor
from src.enrichment.parser import HTMLParserDocument


def test_contact_extraction_emails_and_phones():
    """Verify extraction and normalization of public emails, phones, and contact pages."""
    html = """
    <html>
      <body>
        <p>Email us at <a href="mailto:info@roofingpro.com.au">info@roofingpro.com.au</a> or support@roofingpro.com.au</p>
        <p>Call our office: <a href="tel:0291234567">(02) 9123 4567</a> or mobile <a href="tel:0412345678">0412 345 678</a></p>
        <a href="/contact-us">Contact Us Form</a>
        <address>123 Pitt Street, Sydney NSW 2000, Australia</address>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    extractor = ContactExtractor()
    contacts = extractor.extract(doc, base_url="https://roofingpro.com.au")

    assert "info@roofingpro.com.au" in contacts.emails
    assert "support@roofingpro.com.au" in contacts.emails
    assert "+61291234567" in contacts.phone_numbers
    assert "+61412345678" in contacts.phone_numbers
    assert "https://roofingpro.com.au/contact-us" in contacts.contact_page_urls
    assert len(contacts.physical_addresses) >= 1
    assert "Sydney NSW" in contacts.physical_addresses[0]
