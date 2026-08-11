"""
Unit Tests for AccessibilityAnalyzer.
"""

from src.enrichment.accessibility_analyzer import AccessibilityAnalyzer
from src.enrichment.parser import HTMLParserDocument


def test_accessibility_analyzer_audit():
    """Verify WCAG basic signals audit."""
    html = """
    <html lang="en">
      <body>
        <h1>Title</h1>
        <h2>Section</h2>
        <img src="img.jpg" alt="Description">
        <label for="name">Name</label>
        <input type="text" id="name">
        <a href="/click">Click here</a>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    analyzer = AccessibilityAnalyzer()
    res = analyzer.analyze(doc)

    assert res.data.missing_html_lang is False
    assert res.data.missing_alt_count == 0
    assert res.data.missing_form_labels_count == 0
    assert res.data.generic_anchor_count == 1
    assert res.data.accessibility_score >= 90.0
