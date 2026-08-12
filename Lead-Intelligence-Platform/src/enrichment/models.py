"""
Data Models for Website Intelligence & Deep Technical Analysis (Phase 2).
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class CMSType(str, Enum):
    """Supported CMS Platforms."""
    WORDPRESS = "WordPress"
    SHOPIFY = "Shopify"
    WIX = "Wix"
    SQUARESPACE = "Squarespace"
    WEBFLOW = "Webflow"
    DRUPAL = "Drupal"
    JOOMLA = "Joomla"
    GHOST = "Ghost"
    MAGENTO = "Magento"
    UNKNOWN = "Unknown"


class AnalyzerResult(BaseModel, Generic[T]):
    """Standardized wrapper container for technical analyzer execution outputs."""
    analyzer_name: str = Field(..., description="Name of execution analyzer")
    analyzer_version: str = Field(default="1.0.0", description="Analyzer module version")
    execution_time_seconds: float = Field(default=0.0, description="Analyzer duration in seconds")
    data: T = Field(..., description="Structured analyzer payload")
    findings: list[str] = Field(default_factory=list, description="Key insights or positive findings")
    warnings: list[str] = Field(default_factory=list, description="Non-critical warnings or optimization gaps")
    errors: list[str] = Field(default_factory=list, description="Processing errors encountered")


class FetchResult(BaseModel):
    """Result of HTTP webpage fetch operation."""
    url: str = Field(..., description="Target fetched URL")
    status_code: int = Field(default=0, description="HTTP status code (200, 404, etc.)")
    content: str = Field(default="", description="Decoded HTML/text response body")
    headers: dict[str, str] = Field(default_factory=dict, description="HTTP response headers")
    response_time_ms: float = Field(default=0.0, description="Network round-trip latency in milliseconds")
    is_success: bool = Field(default=False, description="True if status code is 2xx")
    error: str | None = Field(default=None, description="Error message if fetch failed")


class WebsiteMetadata(BaseModel):
    """Extracted HTML document metadata."""
    title: str | None = Field(default=None, description="Page title tag")
    meta_description: str | None = Field(default=None, description="Page meta description")
    canonical_url: str | None = Field(default=None, description="Canonical link URL")
    keywords: list[str] = Field(default_factory=list, description="Meta keywords list")
    open_graph: dict[str, str] = Field(default_factory=dict, description="Open Graph tags (og:title, og:image, etc.)")
    twitter_card: dict[str, str] = Field(default_factory=dict, description="Twitter Card tags")
    h1_tags: list[str] = Field(default_factory=list, description="Extracted H1 headings")
    h2_tags: list[str] = Field(default_factory=list, description="Extracted H2 headings")
    language: str | None = Field(default=None, description="Document language (html lang attribute)")
    charset: str | None = Field(default=None, description="Document character encoding")
    favicon_url: str | None = Field(default=None, description="Discovered favicon link URL")
    generator: str | None = Field(default=None, description="Meta generator tag content")


class ContactIntelligence(BaseModel):
    """Discovered public contact details."""
    emails: list[str] = Field(default_factory=list, description="Extracted public email addresses")
    phone_numbers: list[str] = Field(default_factory=list, description="Extracted and normalized phone numbers")
    contact_page_urls: list[str] = Field(default_factory=list, description="Discovered contact form/page URLs")
    physical_addresses: list[str] = Field(default_factory=list, description="Discovered physical address snippets")


class SocialProfiles(BaseModel):
    """Discovered social media profile links."""
    facebook: str | None = Field(default=None, description="Facebook page URL")
    instagram: str | None = Field(default=None, description="Instagram profile URL")
    linkedin: str | None = Field(default=None, description="LinkedIn company/profile URL")
    twitter_x: str | None = Field(default=None, description="Twitter / X profile URL")
    youtube: str | None = Field(default=None, description="YouTube channel URL")
    tiktok: str | None = Field(default=None, description="TikTok profile URL")
    pinterest: str | None = Field(default=None, description="Pinterest profile URL")


class CMSDetectionResult(BaseModel):
    """CMS platform detection result."""
    cms_name: CMSType = Field(default=CMSType.UNKNOWN, description="Detected CMS platform")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Detection confidence score")
    evidence: list[str] = Field(default_factory=list, description="Signals supporting detection")


class RobotsTxtData(BaseModel):
    """Robots.txt audit and rule data."""
    is_found: bool = Field(default=False, description="True if robots.txt exists (HTTP 200)")
    rules: list[dict[str, str]] = Field(default_factory=list, description="Parsed user-agent disallow/allow rules")
    sitemap_urls: list[str] = Field(default_factory=list, description="Sitemap URLs referenced in robots.txt")
    raw_text: str | None = Field(default=None, description="Raw robots.txt content")


class SitemapData(BaseModel):
    """Sitemap.xml audit data."""
    is_found: bool = Field(default=False, description="True if sitemap XML exists")
    sitemap_urls: list[str] = Field(default_factory=list, description="Discovered XML sitemap URLs")
    url_count: int = Field(default=0, description="Count of URLs listed in sitemap")


# --- Phase 2 Technical & Marketing Intelligence Models ---

class SEOIntelligence(BaseModel):
    """Comprehensive SEO Intelligence Audit Data."""
    title_length: int = Field(default=0)
    is_title_optimal: bool = Field(default=False, description="Title between 30 and 60 chars")
    meta_description_length: int = Field(default=0)
    is_meta_description_optimal: bool = Field(default=False, description="Description between 120 and 160 chars")
    has_meta_keywords: bool = Field(default=False)
    heading_structure_valid: bool = Field(default=False, description="True if exactly 1 H1 tag exists")
    h1_count: int = Field(default=0)
    h2_count: int = Field(default=0)
    canonical_url_valid: bool = Field(default=False)
    is_indexable: bool = Field(default=True, description="True if noindex tag is absent")
    is_followable: bool = Field(default=True, description="True if nofollow tag is absent")
    open_graph_complete: bool = Field(default=False, description="True if og:title and og:image exist")
    twitter_card_complete: bool = Field(default=False, description="True if twitter:card exists")
    image_alt_coverage_ratio: float = Field(default=1.0, ge=0.0, le=1.0, description="Ratio of images with ALT tags")
    total_images: int = Field(default=0)
    missing_alt_images: int = Field(default=0)
    internal_links_count: int = Field(default=0)
    external_links_count: int = Field(default=0)
    has_duplicate_metadata: bool = Field(default=False)


class StructuredDataResult(BaseModel):
    """Structured Data & Schema.org Analysis."""
    detected_formats: list[str] = Field(default_factory=list, description="JSON-LD, Microdata, RDFa")
    detected_schema_types: list[str] = Field(default_factory=list, description="Schema.org types found")
    is_valid: bool = Field(default=False)
    item_count: int = Field(default=0)


class DetectedTechnology(BaseModel):
    """Individual technology detection match."""
    name: str = Field(..., description="Name of technology (e.g. GA4, React, Cloudflare)")
    category: str = Field(..., description="Category classification")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)


class ExpandedTechStack(BaseModel):
    """Comprehensive Multi-Category Technology Intelligence."""
    analytics: list[DetectedTechnology] = Field(default_factory=list)
    advertising: list[DetectedTechnology] = Field(default_factory=list)
    js_frameworks: list[DetectedTechnology] = Field(default_factory=list)
    css_frameworks: list[DetectedTechnology] = Field(default_factory=list)
    infrastructure: list[DetectedTechnology] = Field(default_factory=list)
    marketing_platforms: list[DetectedTechnology] = Field(default_factory=list)
    live_chat: list[DetectedTechnology] = Field(default_factory=list)
    cms: CMSDetectionResult = Field(default_factory=CMSDetectionResult)


class PerformanceIntelligence(BaseModel):
    """Non-browser Performance Audit Data."""
    response_time_ms: float = Field(default=0.0)
    redirect_chain: list[str] = Field(default_factory=list)
    redirect_count: int = Field(default=0)
    http_version: str = Field(default="HTTP/1.1")
    page_size_bytes: int = Field(default=0)
    compression_supported: list[str] = Field(default_factory=list, description="gzip, deflate, br")
    cache_control: str | None = Field(default=None)
    expires: str | None = Field(default=None)
    js_resource_count: int = Field(default=0)
    css_resource_count: int = Field(default=0)
    image_resource_count: int = Field(default=0)
    total_resource_count: int = Field(default=0)


class AccessibilityIntelligence(BaseModel):
    """Lightweight Accessibility Audit Findings."""
    missing_alt_count: int = Field(default=0)
    missing_form_labels_count: int = Field(default=0)
    missing_html_lang: bool = Field(default=False)
    heading_sequence_valid: bool = Field(default=True)
    unlabeled_iframes_count: int = Field(default=0)
    unlabeled_buttons_count: int = Field(default=0)
    generic_anchor_count: int = Field(default=0, description="Links with generic text like 'click here'")
    accessibility_score: float = Field(default=100.0, ge=0.0, le=100.0)


class LinkIntelligence(BaseModel):
    """On-Page Link Distribution and Audit Data."""
    total_links: int = Field(default=0)
    internal_links: list[str] = Field(default_factory=list)
    external_links: list[str] = Field(default_factory=list)
    duplicate_links_count: int = Field(default=0)
    anchor_diversity_score: float = Field(default=1.0, ge=0.0, le=1.0)
    candidate_broken_links: list[str] = Field(default_factory=list, description="Malformed or suspicious URLs")


class PassiveSecurityHeaders(BaseModel):
    """Passive Security Header Audit Signals."""
    has_strict_transport_security: bool = Field(default=False, description="HSTS header present")
    hsts_value: str | None = Field(default=None)
    has_content_security_policy: bool = Field(default=False, description="CSP header present")
    csp_value: str | None = Field(default=None)
    has_x_frame_options: bool = Field(default=False, description="X-Frame-Options present")
    x_frame_options_value: str | None = Field(default=None)
    has_x_content_type_options: bool = Field(default=False, description="nosniff header present")
    has_referrer_policy: bool = Field(default=False)
    has_permissions_policy: bool = Field(default=False)
    security_score: float = Field(default=0.0, ge=0.0, le=100.0)


class CompanyEnrichmentReport(BaseModel):
    """Consolidated report for Phase 2 website and technical intelligence."""
    domain: str = Field(..., description="Target business domain")
    enriched_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Enrichment timestamp"
    )
    fetch_result: FetchResult = Field(..., description="HTTP fetch response metadata")
    metadata: WebsiteMetadata = Field(default_factory=WebsiteMetadata)
    contacts: ContactIntelligence = Field(default_factory=ContactIntelligence)
    socials: SocialProfiles = Field(default_factory=SocialProfiles)
    cms: CMSDetectionResult = Field(default_factory=CMSDetectionResult)
    robots: RobotsTxtData = Field(default_factory=RobotsTxtData)
    sitemap: SitemapData = Field(default_factory=SitemapData)

    # Phase 2 Technical Intelligence Additions
    seo: AnalyzerResult[SEOIntelligence] | None = Field(default=None)
    structured_data: AnalyzerResult[StructuredDataResult] | None = Field(default=None)
    tech_stack: AnalyzerResult[ExpandedTechStack] | None = Field(default=None)
    performance: AnalyzerResult[PerformanceIntelligence] | None = Field(default=None)
    accessibility: AnalyzerResult[AccessibilityIntelligence] | None = Field(default=None)
    links: AnalyzerResult[LinkIntelligence] | None = Field(default=None)
    security: AnalyzerResult[PassiveSecurityHeaders] | None = Field(default=None)

    # Phase 3 Contact Discovery Addition
    contact_discovery: object | None = Field(default=None)

    # Phase 4 Decision Maker Discovery Addition
    decision_maker_discovery: object | None = Field(default=None)

    # Phase 5 Business Intelligence Addition
    business_intelligence: object | None = Field(default=None)

    execution_time_seconds: float = Field(default=0.0, description="Total pipeline processing duration")
    is_successful: bool = Field(default=True, description="True if enrichment completed cleanly")
    notes: list[str] = Field(default_factory=list, description="Warning or execution logs")
