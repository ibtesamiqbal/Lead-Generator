"""
Unit tests for Phase 08 Lead Scoring sub-modules:
SignalExtractor, CategoryWeightCalculator, GradeCalculator, PriorityEngine, ConfidenceEngine, ExplanationEngine.
"""

from src.enrichment.models import CompanyEnrichmentReport, FetchResult
from src.lead_scoring import (
    CategoryWeightCalculator,
    ConfidenceEngine,
    ExplanationEngine,
    GradeCalculator,
    LeadGrade,
    LeadPriority,
    PriorityEngine,
    SignalExtractor,
)


def _dummy_fetch(url: str = "https://example.com") -> FetchResult:
    return FetchResult(url=url, status_code=200, is_success=True)


def test_grade_calculator():
    calc = GradeCalculator()
    assert calc.calculate_grade(95) == LeadGrade.A_PLUS
    assert calc.calculate_grade(87) == LeadGrade.A
    assert calc.calculate_grade(82) == LeadGrade.A_MINUS
    assert calc.calculate_grade(72) == LeadGrade.B
    assert calc.calculate_grade(45) == LeadGrade.F


def test_priority_engine():
    engine = PriorityEngine()
    report = CompanyEnrichmentReport(domain="daikin.com.au", fetch_result=_dummy_fetch())
    priority, purchase, urgency, val = engine.assign_priority_and_potentials(score=88, confidence=0.85, report=report)

    assert priority == LeadPriority.HOT
    assert purchase is not None
    assert urgency is not None
    assert val is not None


def test_confidence_engine():
    engine = ConfidenceEngine()
    report = CompanyEnrichmentReport(domain="testsite.com", fetch_result=_dummy_fetch())
    conf = engine.calculate_confidence(report)

    assert 0.0 <= conf <= 1.0


def test_explanation_engine():
    engine = ExplanationEngine()
    report = CompanyEnrichmentReport(domain="testsite.com", fetch_result=_dummy_fetch())
    pos, neg, codes = engine.generate_explanations(report)

    assert isinstance(pos, list)
    assert isinstance(neg, list)
    assert isinstance(codes, list)


def test_signal_extractor_and_weights():
    extractor = SignalExtractor()
    weight_calc = CategoryWeightCalculator()

    report = CompanyEnrichmentReport(domain="testsite.com", fetch_result=_dummy_fetch())
    breakdown = extractor.extract_category_scores(report)
    score = weight_calc.calculate_composite_score(breakdown)

    assert 0 <= score <= 100
