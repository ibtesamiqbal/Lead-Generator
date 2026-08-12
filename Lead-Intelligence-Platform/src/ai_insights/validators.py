"""
Validator Utilities for Phase 07 — AI Insights & Opportunity Analysis.
"""

import re


class InsightValidator:
    """Utilities for cleaning insight statements and formatting recommendations."""

    @staticmethod
    def clean_text(text: str | None) -> str:
        """Sanitizes text strings for display."""
        if not text or not isinstance(text, str):
            return ""
        return re.sub(r"\s+", " ", text.strip())

    @staticmethod
    def calculate_confidence(available_signals: int, max_expected_signals: int = 6) -> float:
        """Calculates normalized confidence score based on available phase signals."""
        ratio = available_signals / float(max_expected_signals)
        return round(min(0.95, max(0.60, 0.60 + (ratio * 0.35))), 2)
