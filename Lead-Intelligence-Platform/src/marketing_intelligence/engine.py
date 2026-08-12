"""
Master Marketing Intelligence Engine Orchestrator (Phase 06).
Coordinates SEO summary, content intelligence, social presence, conversion funnel,
CTA analysis, marketing tech stack, and digital marketing maturity scoring.
"""

import time
from src.enrichment.models import (
    AnalyzerResult,
    ExpandedTechStack,
    RobotsTxtData,
    SEOIntelligence,
    SitemapData,
    SocialProfiles,
    StructuredDataResult,
    WebsiteMetadata,
)
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger
from src.marketing_intelligence.content import ContentIntelligenceAnalyzer
from src.marketing_intelligence.conversion import ConversionOptimizationAnalyzer
from src.marketing_intelligence.cta import CTAAnalyzer
from src.marketing_intelligence.marketing_tech import MarketingTechDetector
from src.marketing_intelligence.maturity import MarketingMaturityAnalyzer
from src.marketing_intelligence.models import MarketingIntelligenceReport
from src.marketing_intelligence.seo import SEOIntelligenceSummaryAnalyzer
from src.marketing_intelligence.social import SocialPresenceAnalyzer


class MarketingIntelligenceEngine:
    """Orchestrates end-to-end Marketing Intelligence analysis for Phase 06."""

    def __init__(self):
        self.seo_analyzer = SEOIntelligenceSummaryAnalyzer()
        self.content_analyzer = ContentIntelligenceAnalyzer()
        self.social_analyzer = SocialPresenceAnalyzer()
        self.conversion_analyzer = ConversionOptimizationAnalyzer()
        self.cta_analyzer = CTAAnalyzer()
        self.tech_detector = MarketingTechDetector()
        self.maturity_analyzer = MarketingMaturityAnalyzer()

    async def analyze(
        self,
        domain: str,
        doc: HTMLParserDocument | None,
        metadata: WebsiteMetadata | None = None,
        socials: SocialProfiles | None = None,
        seo_result: AnalyzerResult[SEOIntelligence] | None = None,
        structured_data: AnalyzerResult[StructuredDataResult] | None = None,
        tech_stack_result: AnalyzerResult[ExpandedTechStack] | None = None,
        robots: RobotsTxtData | None = None,
        sitemap: SitemapData | None = None,
        source_url: str = ""
    ) -> MarketingIntelligenceReport:
        """
        Synthesizes MarketingIntelligenceReport reusing Phase 02/03/05 outputs.
        """
        start_time = time.perf_counter()
        notes = []

        # 1. SEO Summary
        seo_summary = self.seo_analyzer.summarize_seo(
            metadata=metadata,
            seo_result=seo_result,
            structured_data=structured_data,
            robots=robots,
            sitemap=sitemap
        )

        # 2. Content Intelligence
        content = self.content_analyzer.analyze_content(doc, base_url=source_url)

        # 3. Social Presence
        social = self.social_analyzer.analyze_social(socials)

        # 4. Conversion Funnel Optimization
        conversion = self.conversion_analyzer.analyze_conversion(doc)

        # 5. CTA Analysis
        cta = self.cta_analyzer.analyze_ctas(doc)

        # 6. Marketing Technology Detection
        analytics_tech = self.tech_detector.detect_marketing_tech(tech_stack_result)

        # 7. Marketing Maturity Scoring
        maturity = self.maturity_analyzer.calculate_maturity(
            seo=seo_summary,
            content=content,
            social=social,
            conversion=conversion,
            cta=cta,
            tech=analytics_tech
        )

        report = MarketingIntelligenceReport(
            domain=domain,
            marketing_maturity=maturity,
            seo_summary=seo_summary,
            content=content,
            social=social,
            conversion=conversion,
            cta=cta,
            analytics_tech=analytics_tech,
            overall_score=maturity.score,
            is_successful=True,
            notes=notes
        )

        elapsed = round(time.perf_counter() - start_time, 4)
        logger.info(f"Completed Marketing Intelligence analysis for '{domain}': Maturity={maturity.level.value} ({maturity.score}/100) in {elapsed}s")
        return report
