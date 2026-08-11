"""
Unit Tests for CMSDetector.
"""

from src.enrichment.cms_detector import CMSDetector
from src.enrichment.models import CMSType
from src.enrichment.parser import HTMLParserDocument


def test_cms_detector_wordpress():
    """Verify detection of WordPress platform."""
    html = """
    <html>
      <head>
        <meta name="generator" content="WordPress 6.2">
        <link rel="stylesheet" href="https://example.com/wp-content/themes/main/style.css">
      </head>
    </html>
    """
    doc = HTMLParserDocument(html)
    detector = CMSDetector()
    result = detector.detect(doc)

    assert result.cms_name == CMSType.WORDPRESS
    assert result.confidence >= 0.6
    assert len(result.evidence) >= 1


def test_cms_detector_shopify():
    """Verify detection of Shopify platform."""
    html = """
    <html>
      <head>
        <script src="https://cdn.shopify.com/s/files/1/0000/shopify.js"></script>
      </head>
    </html>
    """
    headers = {"x-shopify-stage": "production"}
    doc = HTMLParserDocument(html)
    detector = CMSDetector()
    result = detector.detect(doc, headers=headers)

    assert result.cms_name == CMSType.SHOPIFY
    assert result.confidence >= 0.7


def test_cms_detector_unknown():
    """Verify detection fallback to Unknown for custom HTML."""
    html = "<html><head><title>Custom Site</title></head><body><h1>Hello</h1></body></html>"
    doc = HTMLParserDocument(html)
    detector = CMSDetector()
    result = detector.detect(doc)

    assert result.cms_name == CMSType.UNKNOWN
    assert result.confidence == 0.0
