"""
Business Model Classifier (Phase 05).
Classifies company business model (B2B, B2C, Both, Non-profit, Government).
"""

import re
from src.business_intelligence.models import BusinessModelType, IndustryCategory
from src.enrichment.parser import HTMLParserDocument


class BusinessModelClassifier:
    """Infers B2B, B2C, Both, Non-profit, or Government based on customer language and industry."""

    def classify_model(
        self,
        doc: HTMLParserDocument | None,
        industry: IndustryCategory
    ) -> BusinessModelType:
        """
        Returns BusinessModelType.
        """
        if not doc or not doc.soup:
            return BusinessModelType.B2B

        text = doc.soup.get_text(separator=" ").lower()

        # Non-profit & Government explicit detection
        if any(kw in text for term in ["non-profit", "501(c)(3)", "charity", "donations", "foundation"] for kw in [term]):
            return BusinessModelType.NON_PROFIT

        if any(kw in text for term in ["gov.au", ".gov", "municipal", "department of", "city council"] for kw in [term]):
            return BusinessModelType.GOVERNMENT

        has_b2b = any(re.search(rf"\b{kw}\b", text) for kw in [
            "b2b", "commercial", "enterprise", "business solutions", "corporate",
            "industrial", "wholesale", "contractor", "organizations", "clients"
        ])

        has_b2c = any(re.search(rf"\b{kw}\b", text) for kw in [
            "b2c", "residential", "homeowners", "home repair", "consumers",
            "patients", "family", "individual", "personal", "book online"
        ])

        # Trade verticals (Roofing, HVAC, Plumbing) typically serve Both (B2B + B2C)
        if industry in (IndustryCategory.ROOFING, IndustryCategory.HVAC, IndustryCategory.PLUMBING, IndustryCategory.ELECTRICAL, IndustryCategory.LANDSCAPING):
            if has_b2b and has_b2c:
                return BusinessModelType.BOTH
            if has_b2b:
                return BusinessModelType.BOTH
            return BusinessModelType.BOTH

        if has_b2b and has_b2c:
            return BusinessModelType.BOTH
        if has_b2c:
            return BusinessModelType.B2C

        return BusinessModelType.B2B
