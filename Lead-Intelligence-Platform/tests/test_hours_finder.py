"""
Unit Tests for BusinessHoursFinder.
"""

from src.contact_discovery.hours_finder import BusinessHoursFinder
from src.enrichment.parser import HTMLParserDocument


def test_business_hours_finder():
    """Verify business operating hours parsing."""
    html = """
    <html>
      <body>
        <p>Trading Hours: Mon - Fri: 8:00 AM - 5:00 PM</p>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    finder = BusinessHoursFinder()
    hours = finder.find_hours(doc, source_url="https://example.com")

    assert hours is not None
    assert "Mon - Fri" in hours.schedule or "General" in hours.schedule
    assert "8:00 AM - 5:00 PM" in str(hours.schedule)
