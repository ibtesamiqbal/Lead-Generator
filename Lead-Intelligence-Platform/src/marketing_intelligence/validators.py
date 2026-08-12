"""
Validator & Normalization Utilities for Marketing Intelligence.
"""

import re


class MarketingValidator:
    """Helper utilities for CTA cleaning, URL validation, and marketing text normalization."""

    INVALID_CTA_PATTERNS = {
        "home", "about", "contact", "privacy", "terms", "cookies", "sitemap",
        "navigation", "menu", "close", "open", "search", "submit", "click here",
        "read story", "learn more about us", "back to top"
    }

    @staticmethod
    def clean_cta_text(text: str | None) -> str:
        """Sanitizes CTA text for display and ranking."""
        if not text or not isinstance(text, str):
            return ""
        cleaned = re.sub(r"\s+", " ", text.strip())
        cleaned = cleaned.rstrip(" >»→.")
        return cleaned.title()

    @classmethod
    def is_valid_cta(cls, text: str | None) -> bool:
        """Validates if string represents a genuine marketing Call-To-Action."""
        if not text or not isinstance(text, str):
            return False
        cleaned = cls.clean_cta_text(text).lower()
        if len(cleaned) < 3 or len(cleaned) > 40:
            return False
        if cleaned in cls.INVALID_CTA_PATTERNS:
            return False
        return True
