"""
Digital Maturity Analyzer (Phase 07).
Combines technical performance, security, SEO, accessibility, and marketing maturity into a single score.
"""

from src.ai_insights.models import DigitalMaturityTier, OverallDigitalMaturity
from src.enrichment.models import CompanyEnrichmentReport


class DigitalMaturityAnalyzer:
    """Calculates overall normalized digital maturity score (0-100) and tier."""

    def calculate_overall_maturity(self, report: CompanyEnrichmentReport) -> OverallDigitalMaturity:
        """
        Synthesizes overall digital maturity score across all phase findings.
        """
        score_components = []

        # 1. Marketing Maturity (Weight 30%)
        if report.marketing_intelligence:
            score_components.append(report.marketing_intelligence.overall_score * 0.30)
        else:
            score_components.append(50.0 * 0.30)

        # 2. SEO Posture (Weight 20%)
        seo_score = 50.0
        if report.seo and report.seo.data:
            d = report.seo.data
            seo_score = (d.heading_structure_valid * 25) + (d.canonical_url_valid * 25) + (d.image_alt_coverage_ratio * 25) + (min(25, d.internal_links_count * 2))
        score_components.append(seo_score * 0.20)

        # 3. Security Score (Weight 15%)
        sec_score = report.security.data.security_score if (report.security and report.security.data) else 50.0
        score_components.append(sec_score * 0.15)

        # 4. Accessibility Score (Weight 15%)
        acc_score = report.accessibility.data.accessibility_score if (report.accessibility and report.accessibility.data) else 50.0
        score_components.append(acc_score * 0.15)

        # 5. Tech Stack & Infrastructure (Weight 20%)
        tech_score = 40.0
        if report.tech_stack and report.tech_stack.data:
            tech_count = len(report.tech_stack.data.analytics) + len(report.tech_stack.data.js_frameworks) + len(report.tech_stack.data.infrastructure)
            tech_score = min(100.0, tech_count * 15.0)
        score_components.append(tech_score * 0.20)

        final_score = int(round(min(100.0, max(0.0, sum(score_components)))))

        if final_score >= 85:
            tier = DigitalMaturityTier.ENTERPRISE
        elif final_score >= 70:
            tier = DigitalMaturityTier.ADVANCED
        elif final_score >= 55:
            tier = DigitalMaturityTier.INTERMEDIATE
        elif final_score >= 40:
            tier = DigitalMaturityTier.DEVELOPING
        else:
            tier = DigitalMaturityTier.BASIC

        return OverallDigitalMaturity(
            level=tier,
            score=final_score,
            confidence=0.90
        )
