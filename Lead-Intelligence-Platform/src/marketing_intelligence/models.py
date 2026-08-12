"""
Pydantic Data Models for Phase 06 — Marketing Intelligence.
Defines schemas for marketing maturity, SEO summary, content assets, social presence,
conversion features, CTA analysis, marketing tech stack, and overall score.
"""

from enum import Enum
from pydantic import BaseModel, Field


class MarketingMaturityLevel(str, Enum):
    BASIC = "Basic"
    DEVELOPING = "Developing"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ENTERPRISE = "Enterprise"


class MarketingMaturity(BaseModel):
    level: MarketingMaturityLevel = MarketingMaturityLevel.BASIC
    score: int = Field(default=0, ge=0, le=100)
    confidence: float = Field(default=0.80, ge=0.0, le=1.0)


class SEOIntelligenceSummary(BaseModel):
    has_title_tag: bool = False
    title_quality: str = "Poor"
    has_meta_description: bool = False
    has_structured_data: bool = False
    has_canonical_tag: bool = False
    has_sitemap: bool = False
    has_robots_txt: bool = False
    heading_hierarchy_valid: bool = False
    image_alt_coverage_ratio: float = 0.0
    internal_linking_rating: str = "Basic"


class ContentIntelligence(BaseModel):
    has_blog: bool = False
    blog_url: str | None = None
    resources_detected: list[str] = Field(default_factory=list)
    has_case_studies: bool = False
    has_whitepapers: bool = False
    has_guides: bool = False
    has_video_content: bool = False
    has_faqs: bool = False
    content_freshness_rating: str = "Unknown"


class SocialPresence(BaseModel):
    has_facebook: bool = False
    facebook_url: str | None = None
    has_linkedin: bool = False
    linkedin_url: str | None = None
    has_instagram: bool = False
    instagram_url: str | None = None
    has_twitter: bool = False
    twitter_url: str | None = None
    has_youtube: bool = False
    youtube_url: str | None = None
    has_tiktok: bool = False
    social_completeness_score: float = Field(default=0.0, ge=0.0, le=100.0)


class ConversionOptimization(BaseModel):
    has_contact_form: bool = False
    has_quote_request: bool = False
    has_demo_request: bool = False
    has_booking_system: bool = False
    has_newsletter_signup: bool = False
    has_live_chat: bool = False
    has_downloadable_assets: bool = False
    conversion_score: float = Field(default=0.0, ge=0.0, le=100.0)


class CTAAnalysis(BaseModel):
    primary_cta: str = "Contact Us"
    secondary_ctas: list[str] = Field(default_factory=list)
    total_ctas_found: int = 0


class MarketingAnalyticsTech(BaseModel):
    has_ga4: bool = False
    has_gtm: bool = False
    has_meta_pixel: bool = False
    has_linkedin_insight: bool = False
    has_hubspot: bool = False
    has_hotjar: bool = False
    has_clarity: bool = False
    detected_marketing_tools: list[str] = Field(default_factory=list)


class MarketingIntelligenceReport(BaseModel):
    domain: str
    marketing_maturity: MarketingMaturity = Field(default_factory=MarketingMaturity)
    seo_summary: SEOIntelligenceSummary = Field(default_factory=SEOIntelligenceSummary)
    content: ContentIntelligence = Field(default_factory=ContentIntelligence)
    social: SocialPresence = Field(default_factory=SocialPresence)
    conversion: ConversionOptimization = Field(default_factory=ConversionOptimization)
    cta: CTAAnalysis = Field(default_factory=CTAAnalysis)
    analytics_tech: MarketingAnalyticsTech = Field(default_factory=MarketingAnalyticsTech)
    overall_score: int = Field(default=0, ge=0, le=100)
    is_successful: bool = True
    notes: list[str] = Field(default_factory=list)
