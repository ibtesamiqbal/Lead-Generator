"""
Signal Extractor Engine (Phase 08).
Extracts normalized feature vectors and sub-scores from Phases 01-07 outputs.
"""

from src.enrichment.models import CompanyEnrichmentReport
from src.lead_scoring.models import CategoryScoreBreakdown


class SignalExtractor:
    """Extracts normalized sub-scores across all 6 enrichment categories."""

    def extract_category_scores(self, report: CompanyEnrichmentReport) -> CategoryScoreBreakdown:
        """
        Calculates category sub-scores (0-100) from pre-computed phase outputs.
        """
        breakdown = CategoryScoreBreakdown()

        # 1. Website Intelligence Sub-Score (0-100)
        web_pts = 0.0
        if report.fetch_result and report.fetch_result.is_success: web_pts += 20.0
        if report.security and report.security.data: web_pts += (report.security.data.security_score * 0.30)
        else: web_pts += 15.0
        if report.accessibility and report.accessibility.data: web_pts += (report.accessibility.data.accessibility_score * 0.30)
        else: web_pts += 15.0
        if report.seo and report.seo.data and report.seo.data.heading_structure_valid: web_pts += 20.0
        breakdown.website_score = round(min(100.0, web_pts), 1)

        # 2. Contact Intelligence Sub-Score (0-100)
        cnt_pts = 0.0
        if report.contacts:
            if report.contacts.emails: cnt_pts += 40.0
            if report.contacts.phone_numbers: cnt_pts += 40.0
            if report.contacts.contact_page_urls: cnt_pts += 20.0
        if report.contact_discovery and report.contact_discovery.addresses: cnt_pts += 10.0
        breakdown.contact_score = round(min(100.0, cnt_pts), 1)

        # 3. Decision Maker Intelligence Sub-Score (0-100)
        dm_pts = 0.0
        if report.decision_maker_discovery:
            dm_count = report.decision_maker_discovery.total_people_found
            if dm_count >= 3: dm_pts += 100.0
            elif dm_count == 2: dm_pts += 80.0
            elif dm_count == 1: dm_pts += 60.0
            else: dm_pts += 10.0
        breakdown.decision_maker_score = round(min(100.0, dm_pts), 1)

        # 4. Business Intelligence Sub-Score (0-100)
        biz_pts = 40.0
        if report.business_intelligence:
            bi = report.business_intelligence
            if bi.company_size_tier:
                tier_val = bi.company_size_tier.value
                if "Small Business" in tier_val or "Mid-Market" in tier_val or "Enterprise" in tier_val:
                    biz_pts += 30.0
            if bi.hiring and bi.hiring.currently_hiring: biz_pts += 20.0
            if bi.trust_signals and (bi.trust_signals.has_testimonials or bi.trust_signals.has_case_studies): biz_pts += 10.0
        breakdown.business_score = round(min(100.0, biz_pts), 1)

        # 5. Marketing Intelligence Sub-Score (0-100)
        if report.marketing_intelligence:
            breakdown.marketing_score = float(report.marketing_intelligence.overall_score)
        else:
            breakdown.marketing_score = 50.0

        # 6. AI Opportunities Sub-Score (0-100)
        ai_pts = 50.0
        if report.ai_insights:
            ai = report.ai_insights
            ai_pts += len(ai.recommended_services) * 15.0
            if ai.digital_maturity:
                ai_pts = (ai_pts * 0.5) + (ai.digital_maturity.score * 0.5)
        breakdown.ai_opportunity_score = round(min(100.0, ai_pts), 1)

        # 7. Confidence Adjustment (-20 to +20)
        conf_adj = 0.0
        if report.fetch_result and report.fetch_result.is_success: conf_adj += 5.0
        if report.decision_maker_discovery and report.decision_maker_discovery.total_people_found > 0: conf_adj += 10.0
        if report.contacts and report.contacts.emails: conf_adj += 5.0
        breakdown.confidence_adjustment = round(conf_adj, 1)

        return breakdown
