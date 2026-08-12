"""
Strengths & Weaknesses Analyzer (Phase 07).
Identifies top business strengths and critical gaps using rule-based signal evaluation.
"""

from src.enrichment.models import CompanyEnrichmentReport


class StrengthsWeaknessesAnalyzer:
    """Evaluates positive signals and technical/digital gaps with supporting evidence."""

    def analyze_strengths_and_weaknesses(self, report: CompanyEnrichmentReport) -> tuple[list[str], list[str]]:
        """
        Returns tuple of (strengths_list, weaknesses_list).
        """
        strengths: list[str] = []
        weaknesses: list[str] = []

        # 1. Technical & Performance
        if report.performance and report.performance.data:
            if report.performance.data.response_time_ms < 1500:
                strengths.append(f"Fast website response latency ({report.performance.data.response_time_ms:.0f}ms)")
            else:
                weaknesses.append(f"Slow website load latency ({report.performance.data.response_time_ms:.0f}ms)")

        # 2. Security Posture
        if report.security and report.security.data:
            if report.security.data.has_strict_transport_security and report.security.data.has_content_security_policy:
                strengths.append("Robust HTTP security posture (HSTS + CSP enabled)")
            elif not report.security.data.has_content_security_policy:
                weaknesses.append("Missing Content Security Policy (CSP) header")

        # 3. SEO & Indexing
        if report.seo and report.seo.data:
            if report.seo.data.canonical_url_valid and report.seo.data.heading_structure_valid:
                strengths.append("Clean SEO structure (Valid H1 hierarchy & canonical tag)")
            if report.seo.data.image_alt_coverage_ratio < 0.60:
                weaknesses.append(f"Poor image ALT tag coverage ({report.seo.data.image_alt_coverage_ratio * 100:.0f}% coverage)")

        # 4. Contact & Decision Makers
        if report.decision_maker_discovery and report.decision_maker_discovery.total_people_found > 0:
            strengths.append(f"Identified {report.decision_maker_discovery.total_people_found} verified decision makers")
        else:
            weaknesses.append("No verified decision makers found on public leadership pages")

        # 5. Marketing & Conversion
        if report.marketing_intelligence:
            mi = report.marketing_intelligence
            if mi.social and mi.social.social_completeness_score >= 75.0:
                strengths.append(f"Strong multi-channel social media footprint ({mi.social.social_completeness_score:.0f}% completeness)")
            elif mi.social and mi.social.social_completeness_score < 50.0:
                weaknesses.append("Incomplete social media channel presence")

            if mi.content and mi.content.has_blog:
                strengths.append("Active blog & content marketing assets detected")
            else:
                weaknesses.append("No blog or content marketing section detected")

            if mi.conversion and mi.conversion.has_live_chat:
                strengths.append("Live chat widget enabled for real-time lead capture")

        # Fallback entries if empty
        if not strengths:
            strengths.append("Accessible public website presence")
        if not weaknesses:
            weaknesses.append("Limited automation & tracking tools detected")

        return (strengths, weaknesses)
