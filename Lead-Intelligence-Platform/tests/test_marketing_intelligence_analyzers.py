"""
Unit tests for Phase 06 Marketing Intelligence sub-analyzers:
SEOIntelligenceSummaryAnalyzer, ContentIntelligenceAnalyzer, SocialPresenceAnalyzer, ConversionOptimizationAnalyzer, CTAAnalyzer, MarketingTechDetector, MarketingMaturityAnalyzer.
"""

from src.enrichment.models import (
    AnalyzerResult,
    DetectedTechnology,
    ExpandedTechStack,
    RobotsTxtData,
    SEOIntelligence,
    SitemapData,
    SocialProfiles,
    StructuredDataResult,
    WebsiteMetadata,
)
from src.enrichment.parser import HTMLParserDocument
from src.marketing_intelligence import (
    ContentIntelligence,
    ContentIntelligenceAnalyzer,
    ConversionOptimization,
    ConversionOptimizationAnalyzer,
    CTAAnalyzer,
    MarketingMaturityAnalyzer,
    MarketingMaturityLevel,
    MarketingTechDetector,
    SEOIntelligenceSummaryAnalyzer,
    SocialPresence,
    SocialPresenceAnalyzer,
)


def test_seo_intelligence_summary_analyzer():
    analyzer = SEOIntelligenceSummaryAnalyzer()
    meta = WebsiteMetadata(title="HubSpot - Software & Marketing Tools", meta_description="Grow better with HubSpot.")
    robots = RobotsTxtData(is_found=True)
    sitemap = SitemapData(sitemap_urls=["https://hubspot.com/sitemap.xml"])

    seo_res = AnalyzerResult[SEOIntelligence](
        analyzer_name="SEO",
        data=SEOIntelligence(canonical_url_valid=True, heading_structure_valid=True, image_alt_coverage_ratio=0.85, internal_links_count=15)
    )
    struct_res = AnalyzerResult[StructuredDataResult](
        analyzer_name="StructuredData",
        data=StructuredDataResult(item_count=2)
    )

    summary = analyzer.summarize_seo(metadata=meta, seo_result=seo_res, structured_data=struct_res, robots=robots, sitemap=sitemap)

    assert summary.has_title_tag is True
    assert summary.title_quality == "Good"
    assert summary.has_meta_description is True
    assert summary.has_robots_txt is True
    assert summary.has_sitemap is True
    assert summary.has_canonical_tag is True
    assert summary.heading_hierarchy_valid is True
    assert summary.internal_linking_rating == "Strong"


def test_content_intelligence_analyzer():
    analyzer = ContentIntelligenceAnalyzer()
    doc = HTMLParserDocument("""
    <html><body>
        <a href="/blog">Our Blog</a>
        <p>Read our case studies and download whitepapers.</p>
        <iframe src="https://www.youtube.com/embed/123"></iframe>
    </body></html>
    """)
    content = analyzer.analyze_content(doc, base_url="https://hubspot.com")

    assert content.has_blog is True
    assert content.blog_url == "https://hubspot.com/blog"
    assert content.has_case_studies is True
    assert content.has_whitepapers is True
    assert content.has_video_content is True


def test_social_presence_analyzer():
    analyzer = SocialPresenceAnalyzer()
    socials = SocialProfiles(facebook="https://facebook.com/hubspot", linkedin="https://linkedin.com/company/hubspot")
    presence = analyzer.analyze_social(socials)

    assert presence.has_facebook is True
    assert presence.has_linkedin is True
    assert presence.social_completeness_score == 50.0


def test_conversion_optimization_analyzer():
    analyzer = ConversionOptimizationAnalyzer()
    doc = HTMLParserDocument("""
    <html><body>
        <form action="/submit"></form>
        <a href="/quote">Request a Quote</a>
        <script src="https://js.intercomcdn.com/intercom.js"></script>
    </body></html>
    """)
    conv = analyzer.analyze_conversion(doc)

    assert conv.has_contact_form is True
    assert conv.has_quote_request is True
    assert conv.has_live_chat is True
    assert conv.conversion_score >= 50.0


def test_cta_analyzer():
    analyzer = CTAAnalyzer()
    doc = HTMLParserDocument("""
    <html><body>
        <a href="/demo" class="btn">Schedule a Demo</a>
        <button class="cta">Contact Us</button>
    </body></html>
    """)
    cta = analyzer.analyze_ctas(doc)

    assert cta.total_ctas_found >= 2
    assert "Schedule A Demo" in cta.primary_cta or "Contact Us" in cta.primary_cta


def test_marketing_tech_detector():
    detector = MarketingTechDetector()
    tech_data = ExpandedTechStack(
        analytics=[DetectedTechnology(name="Google Analytics 4", category="Analytics"), DetectedTechnology(name="Google Tag Manager", category="Analytics")],
        advertising=[DetectedTechnology(name="Meta Pixel", category="Advertising")]
    )
    tech_res = AnalyzerResult[ExpandedTechStack](analyzer_name="TechStack", data=tech_data)

    tech = detector.detect_marketing_tech(tech_res)

    assert tech.has_ga4 is True
    assert tech.has_gtm is True
    assert tech.has_meta_pixel is True
    assert "Google Analytics 4" in tech.detected_marketing_tools


def test_marketing_maturity_analyzer():
    analyzer = MarketingMaturityAnalyzer()
    seo = SEOIntelligenceSummaryAnalyzer().summarize_seo()
    content = ContentIntelligence(has_blog=True, has_case_studies=True)
    social = SocialPresence(has_linkedin=True, has_facebook=True, social_completeness_score=50.0)
    conv = ConversionOptimization(has_contact_form=True, has_quote_request=True, conversion_score=55.0)
    cta = CTAAnalyzer().analyze_ctas(None)
    tech = MarketingTechDetector().detect_marketing_tech(None)

    maturity = analyzer.calculate_maturity(seo, content, social, conv, cta, tech)

    assert maturity.score >= 40
    assert maturity.level in (MarketingMaturityLevel.DEVELOPING, MarketingMaturityLevel.INTERMEDIATE, MarketingMaturityLevel.ADVANCED)
