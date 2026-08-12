"""
Priority Ranking Engine and Confidence Scoring System for Decision Makers (Phase 04).
"""

import re
from src.decision_maker.models import DecisionMaker, Department, Seniority


class DecisionMakerRanker:
    """Calculates priority scores and confidence scores for decision maker candidates."""

    @staticmethod
    def calculate_priority(title: str, department: Department, seniority: Seniority) -> int:
        """
        Calculates priority score (0-100) based on role rank in B2B purchasing decision hierarchy.

        Priority Tiers:
        100: Founder, CEO, Owner, President
        90: Managing Director, Partner, Co-Founder
        80: CTO, COO, CFO, CMO, CIO
        70: VP Sales, Sales Director, Head of Sales, Business Development Director
        60: Operations Director, General Manager, Marketing Director, Growth Director
        50: Other Managers / Directors / Leads
        """
        lower = title.lower()

        is_vp = "vice president" in lower or re.search(r"\bvp\b", lower)

        # Priority 100 Tiers (Top Executives / Founders / Primary Owners)
        if not is_vp:
            if any(term in lower for term in ["founder", "owner", "chief executive"]) or re.search(r"\bceo\b", lower) or re.search(r"\bpresident\b", lower):
                if "co-founder" not in lower and "cofounder" not in lower:
                    return 100

        # Priority 90 Tiers (Co-Founders, Managing Directors, Partners)
        if any(term in lower for term in ["managing director", "partner", "co-founder", "cofounder", "managing partner"]):
            return 90

        # Priority 80 Tiers (C-Suite Technical / Operations / Financial / Marketing Executives)
        if any(re.search(rf"\b{term}\b", lower) for term in ["cto", "coo", "cfo", "cmo", "cio", "chro", "cro"]) or \
           any(term in lower for term in ["chief technology", "chief operating", "chief financial", "chief marketing", "chief information"]):
            return 80

        # Priority 70 Tiers (Sales & Business Development Leadership)
        if any(term in lower for term in [
            "vp sales", "vice president sales", "sales director", "head of sales",
            "business development director", "vp business development", "head of business development"
        ]) or (is_vp and department == Department.SALES):
            return 70

        # Priority 60 Tiers (Operations & Marketing Leadership)
        if any(term in lower for term in [
            "operations director", "general manager", "marketing director", "growth director",
            "head of marketing", "head of operations", "vp marketing", "vp operations"
        ]) or (is_vp and department in (Department.MARKETING, Department.OPERATIONS)):
            return 60

        # Priority 50 (General Director / Manager / VP / Head)
        if seniority in (Seniority.EXECUTIVE, Seniority.VP, Seniority.DIRECTOR, Seniority.HEAD):
            return 50

        return 40

    @staticmethod
    def calculate_confidence(
        is_leadership_page: bool,
        has_recognized_title: bool,
        has_biography: bool,
        multiple_mentions: bool = False,
        has_contact_info: bool = False,
        has_clean_name: bool = True
    ) -> float:
        """
        Calculates confidence score (0.0 to 1.0) using composite extraction signals.
        - Dedicated leadership page: +0.25
        - Recognized executive title: +0.30
        - Clean human name format: +0.15
        - Detailed biography: +0.15
        - Contact details / LinkedIn profile: +0.10
        - Multiple mentions: +0.05
        """
        score = 0.0

        if is_leadership_page:
            score += 0.25

        if has_recognized_title:
            score += 0.30

        if has_clean_name:
            score += 0.15

        if has_biography:
            score += 0.15

        if has_contact_info:
            score += 0.10

        if multiple_mentions:
            score += 0.05

        return round(min(1.0, max(0.0, score)), 2)

    @classmethod
    def rank_decision_makers(cls, candidates: list[DecisionMaker]) -> list[DecisionMaker]:
        """
        Sorts decision makers in descending order of priority score and confidence score.
        """
        return sorted(candidates, key=lambda dm: (dm.priority, dm.confidence), reverse=True)
