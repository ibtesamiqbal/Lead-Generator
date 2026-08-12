"""
Unit tests for Leadership Page Scanner.
"""

from src.decision_maker.website_scanner import LeadershipPageScanner
from src.enrichment.parser import HTMLParserDocument


def test_find_leadership_pages():
    html = """
    <html>
    <head><title>Test Company</title></head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/our-team">Our Leadership Team</a>
            <a href="/services">Services</a>
            <a href="/about-us">About Us</a>
        </nav>
        <footer>
            <a href="/management">Executive Management</a>
        </footer>
    </body>
    </html>
    """
    doc = HTMLParserDocument(html, base_url="https://testcompany.com")
    scanner = LeadershipPageScanner()

    pages = scanner.find_leadership_pages(doc, base_url="https://testcompany.com")
    urls = [p.url for p in pages]

    assert "https://testcompany.com/our-team" in urls
    assert "https://testcompany.com/about-us" in urls
    assert "https://testcompany.com/management" in urls
