"""
Data Models for Contact Discovery Engine (Phase 03).
"""

from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class ConfidenceLevel(str, Enum):
    """Confidence rating for extracted contact data."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class EmailCategory(str, Enum):
    """Classification for business email addresses."""
    GENERAL = "General"
    SALES = "Sales"
    SUPPORT = "Support"
    CAREERS = "Careers"
    MARKETING = "Marketing"
    ACCOUNTS = "Accounts"
    OWNER = "Owner"
    UNKNOWN = "Unknown"


class PhoneCategory(str, Enum):
    """Classification for phone number types."""
    LANDLINE = "Landline"
    MOBILE = "Mobile"
    TOLL_FREE = "TollFree"
    UNKNOWN = "Unknown"


class ContactPageCategory(str, Enum):
    """Classification of secondary contact pages."""
    CONTACT = "Contact"
    ABOUT = "About"
    TEAM = "Team"
    CAREERS = "Careers"
    SUPPORT = "Support"
    QUOTE = "Quote"
    OTHER = "Other"


class ContactEmail(BaseModel):
    """Discovered public email address with confidence rating."""
    address: str = Field(..., description="Normalized email address")
    category: EmailCategory = Field(default=EmailCategory.UNKNOWN)
    source_url: str = Field(..., description="URL where email was discovered")
    discovery_method: str = Field(default="Regex Extraction")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM)
    is_valid_syntax: bool = Field(default=True)


class ContactPhone(BaseModel):
    """Discovered public phone number with E.164 normalization."""
    raw_number: str = Field(..., description="Original raw phone string")
    e164_number: str | None = Field(default=None, description="Normalized E.164 phone string (e.g. +61291234567)")
    formatted_number: str = Field(..., description="Human-readable formatted phone string")
    category: PhoneCategory = Field(default=PhoneCategory.UNKNOWN)
    country_code: str = Field(default="AU", description="ISO country code")
    source_url: str = Field(..., description="URL where phone was discovered")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM)


class BusinessAddress(BaseModel):
    """Extracted physical business address."""
    raw_address: str = Field(..., description="Original raw address snippet")
    street: str | None = Field(default=None)
    city: str | None = Field(default=None)
    state: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    country: str = Field(default="Australia")
    source_url: str = Field(..., description="URL where address was discovered")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MEDIUM)


class BusinessHours(BaseModel):
    """Extracted business operating hours."""
    schedule: dict[str, str] = Field(default_factory=dict, description="e.g. {'Monday-Friday': '8:00 AM - 5:00 PM'}")
    raw_text: str | None = Field(default=None)
    source_url: str = Field(..., description="URL where hours were discovered")


class ContactPage(BaseModel):
    """Discovered secondary contact/team/about page URL."""
    url: str = Field(..., description="Absolute URL of secondary page")
    category: ContactPageCategory = Field(default=ContactPageCategory.OTHER)
    title: str | None = Field(default=None)


class SocialProfileValidation(BaseModel):
    """Validation report for social media profile links."""
    platform: str = Field(..., description="Facebook, Instagram, LinkedIn, etc.")
    url: str = Field(..., description="Profile URL")
    is_valid_format: bool = Field(default=True)
    is_duplicate: bool = Field(default=False)
    has_redirect_parameters: bool = Field(default=False)


class ContactDiscoveryReport(BaseModel):
    """Consolidated report for Contact Discovery Engine (Phase 03)."""
    domain: str = Field(..., description="Target business domain")
    discovered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Discovery timestamp"
    )
    emails: list[ContactEmail] = Field(default_factory=list)
    phones: list[ContactPhone] = Field(default_factory=list)
    addresses: list[BusinessAddress] = Field(default_factory=list)
    operating_hours: BusinessHours | None = Field(default=None)
    contact_pages: list[ContactPage] = Field(default_factory=list)
    social_validations: list[SocialProfileValidation] = Field(default_factory=list)
    total_emails_found: int = Field(default=0)
    total_phones_found: int = Field(default=0)
    execution_time_seconds: float = Field(default=0.0)
    is_successful: bool = Field(default=True)
    notes: list[str] = Field(default_factory=list)
