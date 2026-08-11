"""
Unit Tests for PhoneFinder.
"""

from src.contact_discovery.models import PhoneCategory
from src.contact_discovery.phone_finder import PhoneFinder
from src.enrichment.parser import HTMLParserDocument


def test_phone_finder_e164_normalization():
    """Verify Australian landline, mobile, and toll-free phone extraction and E.164 normalization."""
    html = """
    <html>
      <body>
        <p>Office: <a href="tel:0291234567">(02) 9123 4567</a></p>
        <p>Mobile: 0412 345 678</p>
        <p>Toll Free: 1300 123 456</p>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    finder = PhoneFinder()
    phones = finder.find_phones(doc, source_url="https://apexroofing.com.au")

    e164s = [p.e164_number for p in phones if p.e164_number]
    categories = {p.formatted_number: p.category for p in phones}

    assert "+61291234567" in e164s
    assert "+61412345678" in e164s
    assert any(p.category == PhoneCategory.TOLL_FREE for p in phones)
