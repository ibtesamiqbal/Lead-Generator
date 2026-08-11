"""
Unit Tests for PerformanceAnalyzer.
"""

from src.enrichment.fetcher import FetchResult
from src.enrichment.parser import HTMLParserDocument
from src.enrichment.performance_analyzer import PerformanceAnalyzer


def test_performance_analyzer():
    """Verify performance metrics extraction."""
    html = """
    <html>
      <head>
        <script src="app1.js"></script>
        <script src="app2.js"></script>
        <link rel="stylesheet" href="style.css">
      </head>
      <body>
        <img src="img1.jpg">
        <img src="img2.jpg">
      </body>
    </html>
    """
    fetch_res = FetchResult(
        url="https://example.com",
        status_code=200,
        content=html,
        headers={"Content-Encoding": "gzip", "Cache-Control": "max-age=3600"},
        response_time_ms=150.0,
        is_success=True
    )
    doc = HTMLParserDocument(html)
    analyzer = PerformanceAnalyzer()
    res = analyzer.analyze(fetch_res, doc)

    assert res.data.response_time_ms == 150.0
    assert "gzip" in res.data.compression_supported
    assert res.data.cache_control == "max-age=3600"
    assert res.data.js_resource_count == 2
    assert res.data.css_resource_count == 1
    assert res.data.image_resource_count == 2
    assert res.data.total_resource_count == 5
