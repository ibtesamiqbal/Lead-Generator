"""
Unit Tests for SocialExtractor.
"""

from src.enrichment.parser import HTMLParserDocument
from src.enrichment.social_extractor import SocialExtractor


def test_social_links_extraction():
    """Verify social profile identification and normalization."""
    html = """
    <html>
      <body>
        <a href="https://www.facebook.com/RoofingProAus?utm_source=header">Facebook</a>
        <a href="https://instagram.com/roofingpro_aus/">Instagram</a>
        <a href="https://linkedin.com/company/roofingpro-australia/">LinkedIn</a>
        <a href="https://x.com/roofingproaus">Twitter X</a>
        <a href="https://youtube.com/c/roofingproaus">YouTube</a>
      </body>
    </html>
    """
    doc = HTMLParserDocument(html)
    extractor = SocialExtractor()
    socials = extractor.extract(doc)

    assert socials.facebook == "https://facebook.com/roofingproaus"
    assert socials.instagram == "https://instagram.com/roofingpro_aus"
    assert socials.linkedin == "https://linkedin.com/company/roofingpro-australia"
    assert socials.twitter_x == "https://x.com/roofingproaus"
    assert socials.youtube == "https://youtube.com/c/roofingproaus"
