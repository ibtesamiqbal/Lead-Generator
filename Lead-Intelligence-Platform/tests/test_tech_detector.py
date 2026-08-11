"""
Unit Tests for ExpandedTechDetector.
"""

from src.enrichment.parser import HTMLParserDocument
from src.enrichment.tech_detector import ExpandedTechDetector


def test_expanded_tech_detector():
    """Verify detection of Analytics, Ads, Frameworks, CDN, and Live Chat widgets."""
    html = """
    <html>
      <head>
        <script src="https://www.googletagmanager.com/gtag/js?id=G-12345"></script>
        <script src="https://connect.facebook.net/en_US/fbevents.js"></script>
        <script src="https://widget.intercom.io/widget/app_id"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.0/css/bootstrap.min.css">
      </head>
      <body>
        <div id="__NEXT_DATA__">{}</div>
      </body>
    </html>
    """
    headers = {"cf-ray": "8b1234567890-SYD"}
    doc = HTMLParserDocument(html)
    detector = ExpandedTechDetector()
    res = detector.analyze(doc, headers=headers)

    analytics_names = [t.name for t in res.data.analytics]
    advertising_names = [t.name for t in res.data.advertising]
    js_names = [t.name for t in res.data.js_frameworks]
    infra_names = [t.name for t in res.data.infrastructure]
    chat_names = [t.name for t in res.data.live_chat]

    assert "Google Analytics 4" in analytics_names
    assert "Meta Pixel" in advertising_names
    assert "Next.js" in js_names
    assert "Cloudflare" in infra_names
    assert "Intercom" in chat_names
