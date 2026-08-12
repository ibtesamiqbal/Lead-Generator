"""
Validation & Normalization Utilities for Business Intelligence.
"""

import re


class BusinessIntelligenceValidator:
    """Helper utilities for sanitizing service names, city names, certifications, and years."""

    @staticmethod
    def clean_text(text: str | None) -> str:
        """Cleans and normalizes text whitespace."""
        if not text or not isinstance(text, str):
            return ""
        return re.sub(r"\s+", " ", text.strip())

    @staticmethod
    def extract_year(text: str | None) -> int | None:
        """Extracts plausible founding year (1800-2026) from text string."""
        if not text or not isinstance(text, str):
            return None
        match = re.search(r"\b(18\d{2}|19\d{2}|20[0-2]\d)\b", text)
        if match:
            year = int(match.group(1))
            if 1800 <= year <= 2026:
                return year
        return None
