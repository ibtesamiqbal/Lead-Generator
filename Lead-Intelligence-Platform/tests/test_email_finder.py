"""
Unit Tests for EmailFinder.
"""

from src.contact_discovery.email_finder import EmailFinder
from src.contact_discovery.models import EmailCategory
from src.enrichment.parser import HTMLParserDocument


def test_email_finder_extraction_and_classification():
    """Verify email extraction, classification, and spam trap filtering."""
    html = """
    <html>
      <body>
        <p>General inquiry: info@apexroofing.com.au</p>
        <p>Sales department: <a href="mailto:sales@apexroofing.com.au">sales@apexroofing.com.au</a></p>
        <p>Dummy asset email: logo@2x.png (should be ignored)</p>
        <p>Spam trap: test@example.com (should be ignored)</p>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    finder = EmailFinder()
    emails = finder.find_emails(doc, source_url="https://apexroofing.com.au/contact")

    addrs = [e.address for e in emails]
    categories = {e.address: e.category for e in emails}

    assert "info@apexroofing.com.au" in addrs
    assert "sales@apexroofing.com.au" in addrs
    assert "logo@2x.png" not in addrs
    assert "test@example.com" not in addrs
    assert categories["info@apexroofing.com.au"] == EmailCategory.GENERAL
    assert categories["sales@apexroofing.com.au"] == EmailCategory.SALES
