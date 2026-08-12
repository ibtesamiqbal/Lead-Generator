"""
Pydantic Data Models for Phase 08 — Lead Scoring & Prioritization.
Defines schemas for lead score, letter grade, sales priority, purchase potential,
sales urgency, estimated sales value, category score breakdowns, and reason codes.
"""

from enum import Enum
from pydantic import BaseModel, Field


class LeadGrade(str, Enum):
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    C_PLUS = "C+"
    C = "C"
    D = "D"
    F = "F"


class LeadPriority(str, Enum):
    HOT = "HOT"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    COLD = "COLD"


class PurchasePotential(str, Enum):
    VERY_HIGH = "Very High"
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"
    UNKNOWN = "Unknown"


class SalesUrgency(str, Enum):
    IMMEDIATE = "Immediate"
    HIGH = "High"
    MODERATE = "Moderate"
    LOW = "Low"


class EstimatedSalesValue(str, Enum):
    ENTERPRISE_HIGH = "Enterprise ($50k+)"
    HIGH = "High ($20k-$50k)"
    MEDIUM = "Medium ($10k-$20k)"
    LOW = "Low (<$10k)"


class CategoryScoreBreakdown(BaseModel):
    website_score: float = Field(default=0.0, ge=0.0, le=100.0)
    contact_score: float = Field(default=0.0, ge=0.0, le=100.0)
    decision_maker_score: float = Field(default=0.0, ge=0.0, le=100.0)
    business_score: float = Field(default=0.0, ge=0.0, le=100.0)
    marketing_score: float = Field(default=0.0, ge=0.0, le=100.0)
    ai_opportunity_score: float = Field(default=0.0, ge=0.0, le=100.0)
    confidence_adjustment: float = Field(default=0.0, ge=-20.0, le=20.0)


class LeadScoringReport(BaseModel):
    domain: str
    overall_score: int = Field(default=0, ge=0, le=100, description="Final composite lead score")
    grade: LeadGrade = Field(default=LeadGrade.F, description="Letter grade")
    priority: LeadPriority = Field(default=LeadPriority.COLD, description="Sales priority tier")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Scoring confidence score")
    purchase_potential: PurchasePotential = Field(default=PurchasePotential.UNKNOWN)
    sales_urgency: SalesUrgency = Field(default=SalesUrgency.LOW)
    estimated_sales_value: EstimatedSalesValue = Field(default=EstimatedSalesValue.LOW)
    recommended_contact_role: str = Field(default="Managing Director / Owner")
    recommended_service_bundle: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list, description="Top positive scoring contributors")
    negative_signals: list[str] = Field(default_factory=list, description="Top negative scoring detractors")
    reason_codes: list[str] = Field(default_factory=list, description="Machine-readable audit reason codes")
    category_breakdown: CategoryScoreBreakdown = Field(default_factory=CategoryScoreBreakdown)
    is_successful: bool = True
    notes: list[str] = Field(default_factory=list)
