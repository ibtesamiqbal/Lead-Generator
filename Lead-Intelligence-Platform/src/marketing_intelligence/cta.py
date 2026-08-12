"""
Call-To-Action (CTA) Analyzer (Phase 06).
Extracts and ranks primary and secondary CTAs across webpage DOM buttons, links, and forms.
"""

import re
from src.enrichment.parser import HTMLParserDocument
from src.marketing_intelligence.models import CTAAnalysis
from src.marketing_intelligence.validators import MarketingValidator


class CTAAnalyzer:
    """Extracts, cleans, and ranks primary and secondary Calls-To-Action (CTAs)."""

    PRIORITY_CTA_KEYWORDS = [
        "request a quote", "get a quote", "book now", "schedule a demo",
        "free trial", "get started", "contact us", "call now", "book online",
        "order now", "buy now", "request estimate", "claim offer"
    ]

    def analyze_ctas(self, doc: HTMLParserDocument | None) -> CTAAnalysis:
        """
        Returns populated CTAAnalysis model.
        """
        analysis = CTAAnalysis()
        if not doc or not doc.soup:
            return analysis

        soup = doc.soup
        candidates: set[str] = set()

        # 1. Inspect buttons, input[type=submit], and .btn / .cta elements
        elements = soup.find_all(["button", "a", "input"])
        for el in elements:
            lbl = ""
            if el.name == "input" and el.get("type") in ("submit", "button"):
                lbl = el.get("value") or ""
            else:
                cls_str = " ".join(el.get("class") or []).lower()
                if "btn" in cls_str or "cta" in cls_str or "button" in cls_str or el.name == "button":
                    lbl = el.get_text(strip=True)

            if MarketingValidator.is_valid_cta(lbl):
                cleaned = MarketingValidator.clean_cta_text(lbl)
                candidates.add(cleaned)

        if not candidates:
            # Fallback link text search
            for a in soup.find_all("a"):
                t = a.get_text(strip=True)
                if MarketingValidator.is_valid_cta(t):
                    candidates.add(MarketingValidator.clean_cta_text(t))

        analysis.total_ctas_found = len(candidates)

        # Rank CTAs by priority keyword match
        ranked: list[str] = []
        for kw in self.PRIORITY_CTA_KEYWORDS:
            for c in list(candidates):
                if kw in c.lower() and c not in ranked:
                    ranked.append(c)

        for c in sorted(list(candidates)):
            if c not in ranked:
                ranked.append(c)

        if ranked:
            analysis.primary_cta = ranked[0]
            analysis.secondary_ctas = ranked[1:5]

        return analysis
