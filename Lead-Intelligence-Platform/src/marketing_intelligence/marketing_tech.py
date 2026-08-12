"""
Marketing Technology Detector (Phase 06).
Reuses Phase 02 ExpandedTechStack outputs to detect analytics, pixels, and automation tools.
"""

from src.enrichment.models import ExpandedTechStack, AnalyzerResult
from src.marketing_intelligence.models import MarketingAnalyticsTech


class MarketingTechDetector:
    """Detects GA4, GTM, Meta Pixel, LinkedIn Insight Tag, HubSpot, Hotjar, Microsoft Clarity, etc."""

    def detect_marketing_tech(self, tech_stack_result: AnalyzerResult[ExpandedTechStack] | None = None) -> MarketingAnalyticsTech:
        """
        Synthesizes MarketingAnalyticsTech from Phase 02 TechStack outputs.
        """
        tech = MarketingAnalyticsTech()
        if not tech_stack_result or not tech_stack_result.data:
            return tech

        data = tech_stack_result.data
        tools: set[str] = set()

        all_techs = data.analytics + data.advertising + data.infrastructure + data.js_frameworks

        for t in all_techs:
            name_lower = t.name.lower()
            tools.add(t.name)

            if "google analytics 4" in name_lower or "ga4" in name_lower:
                tech.has_ga4 = True
            elif "google tag manager" in name_lower or "gtm" in name_lower:
                tech.has_gtm = True
            elif "facebook" in name_lower or "meta pixel" in name_lower or "facebook pixel" in name_lower:
                tech.has_meta_pixel = True
            elif "linkedin insight" in name_lower or "linkedin" in name_lower:
                tech.has_linkedin_insight = True
            elif "hubspot" in name_lower:
                tech.has_hubspot = True
            elif "hotjar" in name_lower:
                tech.has_hotjar = True
            elif "microsoft clarity" in name_lower or "clarity" in name_lower:
                tech.has_clarity = True

        tech.detected_marketing_tools = sorted(list(tools))
        return tech
