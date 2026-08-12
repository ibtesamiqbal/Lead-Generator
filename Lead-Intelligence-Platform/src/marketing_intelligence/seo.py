"""
SEO Intelligence Summary Analyzer (Phase 06).
Reuses Phase 02 SEO & Metadata outputs to construct an SEO summary.
"""

from src.enrichment.models import SEOIntelligence, StructuredDataResult, WebsiteMetadata, AnalyzerResult, RobotsTxtData, SitemapData
from src.marketing_intelligence.models import SEOIntelligenceSummary


class SEOIntelligenceSummaryAnalyzer:
    """Summarizes SEO posture reusing Phase 02 analyzer findings."""

    def summarize_seo(
        self,
        metadata: WebsiteMetadata | None = None,
        seo_result: AnalyzerResult[SEOIntelligence] | None = None,
        structured_data: AnalyzerResult[StructuredDataResult] | None = None,
        robots: RobotsTxtData | None = None,
        sitemap: SitemapData | None = None
    ) -> SEOIntelligenceSummary:
        """
        Synthesizes SEOIntelligenceSummary from Phase 02 outputs.
        """
        summary = SEOIntelligenceSummary()

        if metadata:
            if metadata.title:
                summary.has_title_tag = True
                if len(metadata.title) >= 15:
                    summary.title_quality = "Good"
                else:
                    summary.title_quality = "Fair"
            if metadata.meta_description:
                summary.has_meta_description = True

        if robots and robots.is_found:
            summary.has_robots_txt = True
        if sitemap and sitemap.sitemap_urls:
            summary.has_sitemap = True

        if seo_result and seo_result.data:
            d = seo_result.data
            summary.has_canonical_tag = d.canonical_url_valid
            summary.heading_hierarchy_valid = d.heading_structure_valid
            summary.image_alt_coverage_ratio = d.image_alt_coverage_ratio
            if d.internal_links_count >= 10:
                summary.internal_linking_rating = "Strong"
            elif d.internal_links_count >= 3:
                summary.internal_linking_rating = "Good"

        if structured_data and structured_data.data:
            summary.has_structured_data = structured_data.data.item_count > 0

        return summary
