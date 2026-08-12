"""
Configurable Weights & Thresholds Configuration for Phase 08 — Lead Scoring.
Allows custom weighting across all 7 phase scoring categories.
"""

from pydantic import BaseModel, Field


class ScoringWeightsConfig(BaseModel):
    """Configurable Category Weighting Matrix."""
    website_weight: float = Field(default=15.0, ge=0.0, le=100.0)
    contact_weight: float = Field(default=15.0, ge=0.0, le=100.0)
    decision_maker_weight: float = Field(default=20.0, ge=0.0, le=100.0)
    business_weight: float = Field(default=15.0, ge=0.0, le=100.0)
    marketing_weight: float = Field(default=15.0, ge=0.0, le=100.0)
    ai_opportunity_weight: float = Field(default=15.0, ge=0.0, le=100.0)
    confidence_adjustment_weight: float = Field(default=5.0, ge=0.0, le=100.0)

    @property
    def total_weight(self) -> float:
        return (
            self.website_weight +
            self.contact_weight +
            self.decision_maker_weight +
            self.business_weight +
            self.marketing_weight +
            self.ai_opportunity_weight +
            self.confidence_adjustment_weight
        )
