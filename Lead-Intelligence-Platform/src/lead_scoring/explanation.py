"""
Explanation Engine (Phase 08).
Generates positive/negative scoring contributors and machine-readable audit reason codes.
"""

from src.enrichment.models import CompanyEnrichmentReport


class ExplanationEngine:
    """Generates human-readable positive/negative contributors and standardized machine reason codes."""

    REASON_CODES = {
        "EXEC_FOUND": "Verified decision makers identified on leadership page",
        "NO_EXEC_FOUND": "No decision makers identified on public leadership page",
        "VERIFIED_EMAIL": "Public email address discovered",
        "VERIFIED_PHONE": "Public phone number discovered",
        "ACTIVE_HIRING": "Active hiring signals / careers page detected",
        "TRUST_SIGNALS_PRESENT": "Strong trust signals (testimonials, awards, reviews) detected",
        "FAST_LATENCY": "Fast website response latency (<1500ms)",
        "SLOW_LATENCY": "Slow website load latency (>2500ms)",
        "MISSING_CSP": "Missing Content Security Policy (CSP) security header",
        "NO_CONTACT_FORM": "Missing contact or quote request form",
        "LOW_SEO_SCORE": "Poor SEO structure or missing ALT text tags",
        "STRONG_SOCIAL": "High social media footprint completeness (>75%)"
    }

    def generate_explanations(
        self,
        report: CompanyEnrichmentReport
    ) -> tuple[list[str], list[str], list[str]]:
        """
        Returns tuple of (positive_signals, negative_signals, reason_codes).
        """
        positives: list[str] = []
        negatives: list[str] = []
        codes: list[str] = []

        # 1. Decision Makers
        if report.decision_maker_discovery and report.decision_maker_discovery.total_people_found > 0:
            positives.append(f"Identified {report.decision_maker_discovery.total_people_found} verified decision makers")
            codes.append("EXEC_FOUND")
        else:
            negatives.append("No verified decision makers found on public leadership pages")
            codes.append("NO_EXEC_FOUND")

        # 2. Contacts
        if report.contacts and report.contacts.emails:
            positives.append("Public business email address discovered")
            codes.append("VERIFIED_EMAIL")
        if report.contacts and report.contacts.phone_numbers:
            positives.append("Public phone number discovered")
            codes.append("VERIFIED_PHONE")

        # 3. Hiring & Trust
        if report.business_intelligence:
            bi = report.business_intelligence
            if bi.hiring and bi.hiring.currently_hiring:
                positives.append("Active hiring growth signals detected")
                codes.append("ACTIVE_HIRING")
            if bi.trust_signals and (bi.trust_signals.has_testimonials or bi.trust_signals.has_case_studies):
                positives.append("Strong client trust signals (testimonials / case studies) present")
                codes.append("TRUST_SIGNALS_PRESENT")

        # 4. Performance & Security
        if report.performance and report.performance.data:
            if report.performance.data.response_time_ms < 1500:
                positives.append(f"Fast website response latency ({report.performance.data.response_time_ms:.0f}ms)")
                codes.append("FAST_LATENCY")
            elif report.performance.data.response_time_ms > 2500:
                negatives.append(f"Slow website response latency ({report.performance.data.response_time_ms:.0f}ms)")
                codes.append("SLOW_LATENCY")

        if report.security and report.security.data and not report.security.data.has_content_security_policy:
            negatives.append("Missing Content Security Policy (CSP) header")
            codes.append("MISSING_CSP")

        # 5. Conversion & SEO
        if report.marketing_intelligence:
            mi = report.marketing_intelligence
            if mi.conversion and not mi.conversion.has_contact_form and not mi.conversion.has_quote_request:
                negatives.append("Missing online lead form or quote request form")
                codes.append("NO_CONTACT_FORM")
            if mi.social and mi.social.social_completeness_score >= 75.0:
                positives.append("Strong multi-channel social media footprint")
                codes.append("STRONG_SOCIAL")

        if report.seo and report.seo.data and report.seo.data.image_alt_coverage_ratio < 0.60:
            negatives.append("Low image ALT tag coverage ratio (<60%)")
            codes.append("LOW_SEO_SCORE")

        return (positives, negatives, sorted(list(set(codes))))
