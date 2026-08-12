"""
Unit tests for Phase 05 — Business Intelligence Data Models.
"""

from src.business_intelligence.models import (
    BusinessIntelligenceReport,
    BusinessModelType,
    CompanySizeTier,
    GeographicFootprint,
    HiringSignals,
    IndustryCategory,
    TrustSignals,
)


def test_business_intelligence_report_instantiation():
    report = BusinessIntelligenceReport(
        domain="roofingpro.com.au",
        industry=IndustryCategory.ROOFING,
        industry_confidence=0.90,
        business_model=BusinessModelType.BOTH,
        company_size_tier=CompanySizeTier.SMALL_BUSINESS,
        estimated_employee_range="11-50",
        company_size_confidence=0.85,
        founded_year=2008,
        years_in_business=18,
        primary_services=["Roof Repair", "Commercial Roofing"],
        secondary_services=["Guttering", "Maintenance"],
        geography=GeographicFootprint(primary_headquarters="Hervey Bay, QLD", service_areas=["Hervey Bay", "Pialba"]),
        trust_signals=TrustSignals(has_testimonials=True, has_warranty=True),
        hiring=HiringSignals(currently_hiring=False)
    )

    assert report.domain == "roofingpro.com.au"
    assert report.industry == IndustryCategory.ROOFING
    assert report.business_model == BusinessModelType.BOTH
    assert report.years_in_business == 18
    assert "Roof Repair" in report.primary_services
    assert report.trust_signals.has_testimonials is True
    assert report.geography.primary_headquarters == "Hervey Bay, QLD"
