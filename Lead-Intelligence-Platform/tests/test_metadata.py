"""
Unit Tests for MetadataExtractor.
"""

from src.enrichment.metadata import MetadataExtractor
from src.enrichment.parser import HTMLParserDocument


def test_metadata_extraction():
    """Verify extraction of title, meta description, OG tags, canonical URL, and favicon."""
    html = """
    <html lang="en">
      <head>
        <title>Sydney Removalists | Fast & Affordable</title>
        <meta name="description" content="Top rated removal company in Sydney.">
        <meta name="keywords" content="removals, sydney, movers">
        <meta property="og:title" content="Sydney Removalists OG">
        <meta property="og:image" content="https://sydneyremovals.com.au/banner.jpg">
        <meta name="twitter:card" content="summary_large_image">
        <link rel="canonical" href="https://sydneyremovals.com.au/home">
        <link rel="shortcut icon" href="/favicon.ico">
        <meta name="generator" content="WordPress 6.4">
      </head>
      <body>
        <h1>Best Sydney Movers</h1>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    extractor = MetadataExtractor()
    meta = extractor.extract(doc, base_url="https://sydneyremovals.com.au")

    assert meta.title == "Sydney Removalists | Fast & Affordable"
    assert meta.meta_description == "Top rated removal company in Sydney."
    assert meta.canonical_url == "https://sydneyremovals.com.au/home"
    assert meta.keywords == ["removals", "sydney", "movers"]
    assert meta.open_graph["og:title"] == "Sydney Removalists OG"
    assert meta.twitter_card["twitter:card"] == "summary_large_image"
    assert meta.h1_tags == ["Best Sydney Movers"]
    assert meta.language == "en"
    assert meta.favicon_url == "https://sydneyremovals.com.au/favicon.ico"
    assert meta.generator == "WordPress 6.4"
