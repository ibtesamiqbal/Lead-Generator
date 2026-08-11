"""
Unit Tests for LinkAnalyzer.
"""

from src.enrichment.link_analyzer import LinkAnalyzer
from src.enrichment.parser import HTMLParserDocument


def test_link_analyzer_distribution():
    """Verify internal vs external link categorization and malformed link detection."""
    html = """
    <html>
      <body>
        <a href="https://example.com/page1">Internal Page 1</a>
        <a href="https://example.com/page1">Internal Page 1 Duplicate</a>
        <a href="https://external.org">External Org</a>
        <a href="javascript:void(0)">Malformed Link</a>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    analyzer = LinkAnalyzer()
    res = analyzer.analyze(doc, base_url="https://example.com")

    assert res.data.total_links == 4
    assert len(res.data.internal_links) == 1
    assert len(res.data.external_links) == 1
    assert res.data.duplicate_links_count == 1
    assert "javascript:void(0)" in res.data.candidate_broken_links
