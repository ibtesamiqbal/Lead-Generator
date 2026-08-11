"""
Unit Tests for StructuredDataAnalyzer.
"""

from src.enrichment.parser import HTMLParserDocument
from src.enrichment.structured_data_analyzer import StructuredDataAnalyzer


def test_structured_data_analyzer_json_ld():
    """Verify JSON-LD and Microdata schema type extraction."""
    html = """
    <html>
      <head>
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "LocalBusiness",
          "name": "Apex Roofing",
          "address": {
            "@type": "PostalAddress",
            "addressLocality": "Sydney"
          }
        }
        </script>
      </head>
      <body>
        <div itemscope itemtype="https://schema.org/Organization">
          <span itemprop="name">Apex Group</span>
        </div>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    analyzer = StructuredDataAnalyzer()
    res = analyzer.analyze(doc)

    assert res.data.is_valid is True
    assert "JSON-LD" in res.data.detected_formats
    assert "Microdata" in res.data.detected_formats
    assert "LocalBusiness" in res.data.detected_schema_types
    assert "Organization" in res.data.detected_schema_types
    assert "PostalAddress" in res.data.detected_schema_types
    assert res.data.item_count >= 2
