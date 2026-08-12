"""
Grade Calculator (Phase 08).
Maps composite score (0-100) to Letter Grade (A+, A, A-, B+, B, C+, C, D, F).
"""

from src.lead_scoring.models import LeadGrade


class GradeCalculator:
    """Maps composite lead score to letter grade tier."""

    def calculate_grade(self, score: int) -> LeadGrade:
        """
        Score -> Grade Mapping Matrix:
        90-100 -> A+
        85-89  -> A
        80-84  -> A-
        75-79  -> B+
        70-74  -> B
        65-69  -> C+
        60-64  -> C
        50-59  -> D
        < 50   -> F
        """
        if score >= 90:
            return LeadGrade.A_PLUS
        elif score >= 85:
            return LeadGrade.A
        elif score >= 80:
            return LeadGrade.A_MINUS
        elif score >= 75:
            return LeadGrade.B_PLUS
        elif score >= 70:
            return LeadGrade.B
        elif score >= 65:
            return LeadGrade.C_PLUS
        elif score >= 60:
            return LeadGrade.C
        elif score >= 50:
            return LeadGrade.D
        else:
            return LeadGrade.F
