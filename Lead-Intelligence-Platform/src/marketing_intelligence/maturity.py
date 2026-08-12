"""
Marketing Maturity Analyzer (Phase 06).
Calculates composite digital marketing maturity score (0-100) and level classification.
"""

from src.marketing_intelligence.models import (
    ContentIntelligence,
    ConversionOptimization,
    CTAAnalysis,
    MarketingAnalyticsTech,
    MarketingMaturity,
    MarketingMaturityLevel,
    SEOIntelligenceSummary,
    SocialPresence,
)


class MarketingMaturityAnalyzer:
    """Calculates weighted overall marketing maturity score (0-100) and assigns maturity level."""

    def calculate_maturity(
        self,
        seo: SEOIntelligenceSummary,
        content: ContentIntelligence,
        social: SocialPresence,
        conversion: ConversionOptimization,
        cta: CTAAnalysis,
        tech: MarketingAnalyticsTech
    ) -> MarketingMaturity:
        """
        Returns populated MarketingMaturity model.
        """
        score = 0.0

        # 1. SEO Posture (20 pts max)
        if seo.has_title_tag: score += 5.0
        if seo.has_meta_description: score += 5.0
        if seo.has_structured_data: score += 5.0
        if seo.has_sitemap or seo.has_robots_txt: score += 5.0

        # 2. Content & Assets (20 pts max)
        if content.has_blog: score += 8.0
        if content.has_case_studies: score += 6.0
        if content.has_guides or content.has_whitepapers or content.has_video_content: score += 6.0

        # 3. Social Presence (15 pts max)
        score += (social.social_completeness_score / 100.0) * 15.0

        # 4. Conversion Funnel (20 pts max)
        if conversion.has_contact_form: score += 8.0
        if conversion.has_quote_request or conversion.has_demo_request: score += 6.0
        if conversion.has_live_chat or conversion.has_booking_system: score += 6.0

        # 5. CTA Clarity (10 pts max)
        if cta.primary_cta: score += 6.0
        if cta.total_ctas_found > 0: score += 4.0

        # 6. Analytics & Tech Stack (15 pts max)
        if tech.has_ga4 or tech.has_gtm: score += 8.0
        if tech.has_meta_pixel or tech.has_linkedin_insight or tech.has_hubspot: score += 7.0

        final_score = int(round(min(100.0, max(0.0, score))))

        if final_score >= 85:
            level = MarketingMaturityLevel.ENTERPRISE
        elif final_score >= 70:
            level = MarketingMaturityLevel.ADVANCED
        elif final_score >= 50:
            level = MarketingMaturityLevel.INTERMEDIATE
        elif final_score >= 30:
            level = MarketingMaturityLevel.DEVELOPING
        else:
            level = MarketingMaturityLevel.BASIC

        return MarketingMaturity(
            level=level,
            score=final_score,
            confidence=0.88
        )
