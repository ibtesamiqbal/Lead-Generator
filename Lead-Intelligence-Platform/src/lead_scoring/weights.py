"""
Weighted Category Scoring Engine (Phase 08).
Applies configurable category weights to sub-scores and calculates composite score.
"""

from src.lead_scoring.config import ScoringWeightsConfig
from src.lead_scoring.models import CategoryScoreBreakdown
from src.lead_scoring.validators import LeadScoringValidator


class CategoryWeightCalculator:
    """Calculates weighted composite score using configurable weight matrix."""

    def calculate_composite_score(
        self,
        breakdown: CategoryScoreBreakdown,
        config: ScoringWeightsConfig | None = None
    ) -> int:
        """
        Returns normalized 0-100 composite integer lead score.
        """
        cfg = config or ScoringWeightsConfig()
        total_w = cfg.total_weight

        weighted_sum = (
            (breakdown.website_score * cfg.website_weight) +
            (breakdown.contact_score * cfg.contact_weight) +
            (breakdown.decision_maker_score * cfg.decision_maker_weight) +
            (breakdown.business_score * cfg.business_weight) +
            (breakdown.marketing_score * cfg.marketing_weight) +
            (breakdown.ai_opportunity_score * cfg.ai_opportunity_weight)
        )

        base_score = weighted_sum / max(1.0, (total_w - cfg.confidence_adjustment_weight))
        final_score = base_score + breakdown.confidence_adjustment

        return LeadScoringValidator.clamp_score(final_score)
