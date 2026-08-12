"""
Pydantic Data Models for Phase 07 — AI Insights & Opportunity Analysis.
Defines schemas for executive summary, overall digital maturity, strengths/weaknesses,
opportunities, recommended services, outreach strategy, risk assessment, and overall confidence.
"""

from enum import Enum
from pydantic import BaseModel, Field


class DigitalMaturityTier(str, Enum):
    BASIC = "Basic"
    DEVELOPING = "Developing"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    ENTERPRISE = "Enterprise"


class OverallDigitalMaturity(BaseModel):
    level: DigitalMaturityTier = DigitalMaturityTier.BASIC
    score: int = Field(default=0, ge=0, le=100)
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)


class OpportunityBreakdown(BaseModel):
    seo: list[str] = Field(default_factory=list, description="SEO enhancement opportunities")
    marketing: list[str] = Field(default_factory=list, description="Marketing & content opportunities")
    conversion: list[str] = Field(default_factory=list, description="Conversion rate optimization opportunities")
    sales: list[str] = Field(default_factory=list, description="Sales enablement opportunities")


class RecommendedServiceItem(BaseModel):
    service_name: str = Field(..., description="Recommended agency/tech service")
    priority: str = Field(default="Medium", description="High, Medium, Low")
    rationale: str = Field(..., description="Explainable justification referencing signal evidence")
    supporting_signals: list[str] = Field(default_factory=list)


class OutreachStrategy(BaseModel):
    primary_contact_target: str = Field(default="Managing Director / Owner")
    suggested_tone: str = Field(default="Consultative")
    opening_angle: str = Field(default="Consultative growth opportunity audit", description="Tailored opening hook for cold outreach")
    talking_points: list[str] = Field(default_factory=list, description="Key pitch talking points")


class AIInsightsReport(BaseModel):
    domain: str
    executive_summary: str = Field(..., description="Concise multi-sentence business summary")
    digital_maturity: OverallDigitalMaturity = Field(default_factory=OverallDigitalMaturity)
    strengths: list[str] = Field(default_factory=list, description="Validated business & digital strengths")
    weaknesses: list[str] = Field(default_factory=list, description="Identified technical & digital gaps")
    opportunities: OpportunityBreakdown = Field(default_factory=OpportunityBreakdown)
    recommended_services: list[RecommendedServiceItem] = Field(default_factory=list)
    outreach_strategy: OutreachStrategy = Field(default_factory=OutreachStrategy)
    risks: list[str] = Field(default_factory=list, description="Identified risk factors or signal uncertainties")
    confidence: float = Field(default=0.88, ge=0.0, le=1.0, description="Composite AI analysis confidence score")
    is_successful: bool = True
    notes: list[str] = Field(default_factory=list)
