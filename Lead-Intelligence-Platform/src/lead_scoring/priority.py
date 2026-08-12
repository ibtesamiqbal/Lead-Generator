"""
Priority Engine (Phase 08).
Assigns Sales Priority (HOT, HIGH, MEDIUM, LOW, COLD), Purchase Potential, Sales Urgency,
and Estimated Sales Value supported by enrichment evidence.
"""

from src.enrichment.models import CompanyEnrichmentReport
from src.lead_scoring.models import EstimatedSalesValue, LeadPriority, PurchasePotential, SalesUrgency


class PriorityEngine:
    """Evaluates composite score, confidence, and business size signals to assign sales urgency & priority."""

    def assign_priority_and_potentials(
        self,
        score: int,
        confidence: float,
        report: CompanyEnrichmentReport
    ) -> tuple[LeadPriority, PurchasePotential, SalesUrgency, EstimatedSalesValue]:
        """
        Returns tuple of (LeadPriority, PurchasePotential, SalesUrgency, EstimatedSalesValue).
        """
        # 1. Lead Priority Assignment
        if score >= 85 and confidence >= 0.75:
            priority = LeadPriority.HOT
        elif score >= 75:
            priority = LeadPriority.HIGH
        elif score >= 60:
            priority = LeadPriority.MEDIUM
        elif score >= 45:
            priority = LeadPriority.LOW
        else:
            priority = LeadPriority.COLD

        # 2. Purchase Potential
        if score >= 80:
            purchase_potential = PurchasePotential.VERY_HIGH
        elif score >= 65:
            purchase_potential = PurchasePotential.HIGH
        elif score >= 50:
            purchase_potential = PurchasePotential.MODERATE
        else:
            purchase_potential = PurchasePotential.LOW

        # 3. Sales Urgency
        hiring_signal = report.business_intelligence and report.business_intelligence.hiring and report.business_intelligence.hiring.currently_hiring
        dm_signal = report.decision_maker_discovery and report.decision_maker_discovery.total_people_found > 0

        if priority in (LeadPriority.HOT, LeadPriority.HIGH) and hiring_signal and dm_signal:
            sales_urgency = SalesUrgency.IMMEDIATE
        elif priority in (LeadPriority.HOT, LeadPriority.HIGH):
            sales_urgency = SalesUrgency.HIGH
        elif priority == LeadPriority.MEDIUM:
            sales_urgency = SalesUrgency.MODERATE
        else:
            sales_urgency = SalesUrgency.LOW

        # 4. Estimated Sales Value
        est_val = EstimatedSalesValue.MEDIUM
        if report.business_intelligence and report.business_intelligence.company_size_tier:
            size_val = report.business_intelligence.company_size_tier.value
            if "Enterprise" in size_val or "Mid-Market" in size_val:
                est_val = EstimatedSalesValue.ENTERPRISE_HIGH
            elif "Small Business" in size_val:
                est_val = EstimatedSalesValue.HIGH
            elif "Micro" in size_val:
                est_val = EstimatedSalesValue.MEDIUM
            else:
                est_val = EstimatedSalesValue.LOW

        return (priority, purchase_potential, sales_urgency, est_val)
