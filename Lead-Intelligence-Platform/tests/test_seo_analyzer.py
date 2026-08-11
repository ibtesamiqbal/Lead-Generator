"""
Unit Tests for SEOAnalyzer.
"""

from src.enrichment.parser import HTMLParserDocument
from src.enrichment.seo_analyzer import SEOAnalyzer


def test_seo_analyzer_optimal_title_and_description():
    """Verify auditing of title length, meta description, heading structure, canonical link, and OpenGraph completeness."""
    html = """
    <html lang="en">
      <head>
        <title>Sydney Premium Removalists Services for Office & Home</title>
        <meta name="description" content="Professional and reliable removalist services in Sydney. Fast packing, relocation, and insured transport for residential homes.">
        <meta property="og:title" content="Sydney Removalists">
        <meta property="og:image" content="https://example.com/banner.jpg">
        <link rel="canonical" href="https://example.com/">
      </head>
      <body>
        <h1>Sydney Relocation Specialists</h1>
        <h2>Home Removal</h2>
        <h2>Office Removal</h2>
        <img src="logo.png" alt="Company Logo">
        <a href="https://example.com/about">About</a>
        <a href="https://google.com">Google</a>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    analyzer = SEOAnalyzer()
    res = analyzer.analyze(doc, base_url="https://example.com")

    assert res.data.is_title_optimal is True
    assert res.data.is_meta_description_optimal is True
    assert res.data.heading_structure_valid is True
    assert res.data.h1_count == 1
    assert res.data.h2_count == 2
    assert res.data.canonical_url_valid is True
    assert res.data.open_graph_complete is True
    assert res.data.image_alt_coverage_ratio == 1.0
    assert res.data.internal_links_count == 1
    assert res.data.external_links_count == 1
