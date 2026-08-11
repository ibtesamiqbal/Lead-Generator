"""
Unit Tests for HTMLParserDocument.
"""

from src.enrichment.parser import HTMLParserDocument


def test_html_parser_title():
    """Verify title tag parsing."""
    doc = HTMLParserDocument("<html><head><title> Roofing Pro Australia </title></head></html>")
    assert doc.get_title() == "Roofing Pro Australia"


def test_html_parser_meta():
    """Verify meta description and property parsing."""
    html = """
    <html>
      <head>
        <meta name="description" content="Premier roofing services in Sydney.">
        <meta property="og:title" content="Roofing Pro OG Title">
      </head>
    </html>
    """
    doc = HTMLParserDocument(html)
    assert doc.get_meta_content("description") == "Premier roofing services in Sydney."
    assert doc.get_meta_content("og:title") == "Roofing Pro OG Title"


def test_html_parser_headings():
    """Verify heading tags parsing."""
    html = "<html><body><h1>Main Heading</h1><h2>Sub Heading 1</h2><h2>Sub Heading 2</h2></body></html>"
    doc = HTMLParserDocument(html)
    assert doc.get_headings("h1") == ["Main Heading"]
    assert doc.get_headings("h2") == ["Sub Heading 1", "Sub Heading 2"]


def test_html_parser_links():
    """Verify link extraction."""
    html = '<html><body><a href="https://example.com/about">About Us</a></body></html>'
    doc = HTMLParserDocument(html)
    links = doc.get_all_links()
    assert len(links) == 1
    assert links[0]["href"] == "https://example.com/about"
    assert links[0]["text"] == "About Us"
