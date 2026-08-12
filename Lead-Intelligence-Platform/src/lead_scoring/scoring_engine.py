"""
Scoring Engine (Phase 08).
Executes signal extraction, weighted scoring, grade mapping, priority classification,
confidence calculation, explanation generation, and recommendation synthesis.
"""

from src.enrichment.models import CompanyEnrichmentReport
from src.lead_scoring.config import ScoringWeightsConfig
from src.lead_scoring.confidence import ConfidenceEngine
from src.lead_scoring.explanation import ExplanationEngine
from src.lead_scoring.grading import GradeCalculator
from src.lead_scoring.models import LeadScoringReport
from src.lead_scoring.priority import PriorityEngine
from src.lead_scoring.signal_extractors import SignalExtractor
from src.lead_scoring.weights import CategoryWeightCalculator


class ScoringEngine:
    """Core lead scoring execution logic."""

    def __init__(self, config: ScoringWeightsConfig | None = None):
        self.config = config or ScoringWeightsConfig()
        self.signal_extractor = SignalExtractor()
        self.weight_calculator = CategoryWeightCalculator()
        self.grade_calculator = GradeCalculator()
        self.priority_engine = PriorityEngine()
        self.confidence_engine = ConfidenceEngine()
        self.explanation_engine = ExplanationEngine()

    def score_report(self, report: CompanyEnrichmentReport) -> LeadScoringReport:
        """
        Processes enrichment report into deterministic LeadScoringReport.
        """
        # 1. Extract category sub-scores
        category_breakdown = self.signal_extractor.extract_category_scores(report)

        # 2. Calculate overall weighted score
        overall_score = self.weight_calculator.calculate_composite_score(category_breakdown, self.config)

        # 3. Calculate confidence score
        confidence = self.confidence_engine.calculate_confidence(report)

        # 4. Map score to letter grade
        grade = self.grade_calculator.calculate_grade(overall_score)

        # 5. Assign sales priority & potentials
        priority, purchase_pot, sales_urg, est_val = self.priority_engine.assign_priority_and_potentials(
            score=overall_score,
            confidence=confidence,
            report=report
        )

        # 6. Generate explanations & reason codes
        positives, negatives, reason_codes = self.explanation_engine.generate_explanations(report)

        # 7. Extract recommended contact role & service bundle
        contact_role = "Managing Director / Owner"
        service_bundle = ["Website Optimization", "SEO Audit"]

        if report.ai_insights:
            ai = report.ai_insights
            if ai.outreach_strategy and ai.outreach_strategy.primary_contact_target:
                contact_role = ai.outreach_strategy.primary_contact_target
            if ai.recommended_services:
                service_bundle = [s.service_name for s in ai.recommended_services]

        return LeadScoringReport(
            domain=report.domain,
            overall_score=overall_score,
            grade=grade,
            priority=priority,
            confidence=confidence,
            purchase_potential=purchase_pot,
            sales_urgency=sales_urg,
            estimated_sales_value=est_val,
            recommended_contact_role=contact_role,
            recommended_service_bundle=service_bundle,
            positive_signals=positives,
            negative_signals=negatives,
            reason_codes=reason_codes,
            category_breakdown=category_breakdown,
            is_successful=True,
            notes=[]
        )
