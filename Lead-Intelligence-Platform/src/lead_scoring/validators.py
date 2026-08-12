"""
Validator Utilities for Phase 08 — Lead Scoring & Prioritization.
"""


class LeadScoringValidator:
    """Helper utilities for score normalization, bounds enforcement, and signal checks."""

    @staticmethod
    def clamp_score(score: float | int) -> int:
        """Clamps score integer within [0, 100]."""
        return int(round(min(100.0, max(0.0, float(score)))))

    @staticmethod
    def clamp_confidence(conf: float) -> float:
        """Clamps confidence float within [0.0, 1.0]."""
        return round(min(1.0, max(0.0, conf)), 2)
