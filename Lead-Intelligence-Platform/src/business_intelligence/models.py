"""
Pydantic Data Models for Phase 05 — Business Intelligence.
Defines structured schemas for industry classification, services, geography,
company size, business model, trust signals, and hiring signals.
"""

from enum import Enum
from pydantic import BaseModel, Field


class IndustryCategory(str, Enum):
    ROOFING = "Roofing"
    HVAC = "HVAC"
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    LANDSCAPING = "Landscaping"
    SAAS = "SaaS"
    MARKETING_AGENCY = "Marketing Agency"
    LAW_FIRM = "Law Firm"
    DENTAL_CLINIC = "Dental Clinic"
    MANUFACTURING = "Manufacturing"
    FINANCIAL_SERVICES = "Financial Services"
    HEALTHCARE = "Healthcare"
    REAL_ESTATE = "Real Estate"
    CONSTRUCTION = "Construction"
    OTHER_B2B = "Other B2B"


class BusinessModelType(str, Enum):
    B2B = "B2B"
    B2C = "B2C"
    BOTH = "B2B + B2C"
    NON_PROFIT = "Non-Profit"
    GOVERNMENT = "Government"


class CompanySizeTier(str, Enum):
    SOLOPRENEUR_MICRO = "Micro (1-10)"
    SMALL_BUSINESS = "Small Business (11-50)"
    MID_MARKET = "Mid-Market (51-250)"
    ENTERPRISE = "Enterprise (251+)"


class TrustSignals(BaseModel):
    has_testimonials: bool = False
    has_reviews: bool = False
    has_case_studies: bool = False
    has_portfolio: bool = False
    has_financing: bool = False
    has_warranty: bool = False
    certifications: list[str] = Field(default_factory=list)
    awards: list[str] = Field(default_factory=list)


class HiringSignals(BaseModel):
    currently_hiring: bool = False
    has_careers_page: bool = False
    careers_page_url: str | None = None
    open_roles_detected: list[str] = Field(default_factory=list)


class GeographicFootprint(BaseModel):
    primary_headquarters: str | None = None
    service_areas: list[str] = Field(default_factory=list)
    states_served: list[str] = Field(default_factory=list)
    office_locations_count: int = 1


class BusinessIntelligenceReport(BaseModel):
    domain: str
    industry: IndustryCategory = IndustryCategory.OTHER_B2B
    industry_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    business_model: BusinessModelType = BusinessModelType.B2B
    company_size_tier: CompanySizeTier = CompanySizeTier.SMALL_BUSINESS
    estimated_employee_range: str = "11-50"
    company_size_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    founded_year: int | None = None
    years_in_business: int | None = None
    primary_services: list[str] = Field(default_factory=list)
    secondary_services: list[str] = Field(default_factory=list)
    geography: GeographicFootprint = Field(default_factory=GeographicFootprint)
    trust_signals: TrustSignals = Field(default_factory=TrustSignals)
    hiring: HiringSignals = Field(default_factory=HiringSignals)
    is_successful: bool = True
    notes: list[str] = Field(default_factory=list)
