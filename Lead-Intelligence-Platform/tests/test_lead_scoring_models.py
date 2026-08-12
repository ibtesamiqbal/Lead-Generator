"""
Unit tests for Phase 08 — Lead Scoring & Prioritization Data Models & Config.
"""

from src.lead_scoring.config import ScoringWeightsConfig
from src.lead_scoring.models import (
    CategoryScoreBreakdown,
    EstimatedSalesValue,
    LeadGrade,
    LeadPriority,
    LeadScoringReport,
    PurchasePotential,
    SalesUrgency,
)


def test_scoring_weights_config_defaults():
    cfg = ScoringWeightsConfig()
    assert cfg.website_weight == 15.0
    assert cfg.decision_maker_weight == 20.0
    assert cfg.total_weight == 100.0


def test_lead_scoring_report_instantiation():
    report = LeadScoringReport(
        domain="daikin.com.au",
        overall_score=88,
        grade=LeadGrade.A,
        priority=LeadPriority.HOT,
        confidence=0.92,
        purchase_potential=PurchasePotential.VERY_HIGH,
        sales_urgency=SalesUrgency.HIGH,
        estimated_sales_value=EstimatedSalesValue.HIGH,
        recommended_contact_role="General Manager",
        recommended_service_bundle=["CRO", "SEO"],
        positive_signals=["Executive identified"],
        negative_signals=["Missing CSP"],
        reason_codes=["EXEC_FOUND", "MISSING_CSP"],
        category_breakdown=CategoryScoreBreakdown(website_score=75.0, decision_maker_score=80.0)
    )

    assert report.domain == "daikin.com.au"
    assert report.overall_score == 88
    assert report.grade == LeadGrade.A
    assert report.priority == LeadPriority.HOT
    assert "EXEC_FOUND" in report.reason_codes
