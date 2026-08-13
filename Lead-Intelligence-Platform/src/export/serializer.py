"""
Centralized Enrichment Serializer (Phase 09).
Flattens nested CompanyEnrichmentReport models into export-friendly flat dictionaries,
relational database tables, and normalized JSON structures without duplicating transformation logic.
"""

from datetime import datetime, timezone
from typing import Any
from src.enrichment.models import CompanyEnrichmentReport
from src.export.models import FlatCompanyRecord


class EnrichmentSerializer:
    """Centralized transformer converting CompanyEnrichmentReport objects into flat export structures."""

    def to_flat_record(self, report: CompanyEnrichmentReport) -> FlatCompanyRecord:
        """
        Converts CompanyEnrichmentReport into a normalized 1-row FlatCompanyRecord.
        """
        domain = report.domain
        company_title = (report.metadata.title if report.metadata else "") or domain
        cms_val = report.cms.cms_name.value if (report.cms and hasattr(report.cms.cms_name, "value")) else "Unknown"

        # Industry & Business
        ind = "Other B2B"
        size_tier = "Small Business (11-50)"
        est_emp = "11-50"
        if report.business_intelligence:
            if report.business_intelligence.industry:
                ind = report.business_intelligence.industry.value
            if report.business_intelligence.company_size_tier:
                size_tier = report.business_intelligence.company_size_tier.value
            if report.business_intelligence.estimated_employee_range:
                est_emp = report.business_intelligence.estimated_employee_range

        # Lead Scoring
        score = 0
        grade = "F"
        priority = "COLD"
        conf = 0.0
        pot = "Unknown"
        urg = "Low"
        val = "Low"
        role = "Managing Director / Owner"
        recs_str = ""
        pos_str = ""
        neg_str = ""
        codes_str = ""

        if report.lead_scoring:
            ls = report.lead_scoring
            score = ls.overall_score
            grade = ls.grade.value
            priority = ls.priority.value
            conf = ls.confidence
            pot = ls.purchase_potential.value
            urg = ls.sales_urgency.value
            val = ls.estimated_sales_value.value
            role = ls.recommended_contact_role
            recs_str = ", ".join(ls.recommended_service_bundle)
            pos_str = "; ".join(ls.positive_signals)
            neg_str = "; ".join(ls.negative_signals)
            codes_str = ", ".join(ls.reason_codes)

        # Decision Makers
        dm_count = 0
        top_dm = "None"
        if report.decision_maker_discovery:
            dm_count = report.decision_maker_discovery.total_people_found
            if report.decision_maker_discovery.decision_makers:
                first = report.decision_maker_discovery.decision_makers[0]
                top_dm = f"{first.full_name} ({first.title})"

        # Contacts
        emails_str = ""
        phones_str = ""
        if report.contacts:
            emails_str = ", ".join(report.contacts.emails)
            phones_str = ", ".join(report.contacts.phone_numbers)

        # Marketing
        mkt_maturity = "Basic"
        mkt_score = 0
        primary_cta = "None"
        if report.marketing_intelligence:
            mkt = report.marketing_intelligence
            mkt_maturity = mkt.marketing_maturity.level.value
            mkt_score = mkt.overall_score
            primary_cta = mkt.cta.primary_cta

        return FlatCompanyRecord(
            domain=domain,
            company_title=company_title,
            cms_name=cms_val,
            industry=ind,
            company_size_tier=size_tier,
            estimated_employees=est_emp,
            overall_lead_score=score,
            grade=grade,
            priority=priority,
            confidence=conf,
            purchase_potential=pot,
            sales_urgency=urg,
            estimated_sales_value=val,
            target_contact_role=role,
            decision_makers_count=dm_count,
            top_decision_maker=top_dm,
            contact_emails=emails_str,
            contact_phones=phones_str,
            marketing_maturity=mkt_maturity,
            marketing_score=mkt_score,
            primary_cta=primary_cta,
            recommended_services=recs_str,
            positive_signals=pos_str,
            negative_signals=neg_str,
            reason_codes=codes_str,
            exported_at=datetime.now(timezone.utc).isoformat()
        )

    def to_dict(self, report: CompanyEnrichmentReport) -> dict[str, Any]:
        """Converts report to dictionary via Pydantic model dump."""
        return report.model_dump(mode="json")
