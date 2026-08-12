"""
Data Models for Decision Maker Discovery Engine (Phase 04).
"""

import uuid
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


class Department(str, Enum):
    """Business department classification."""
    EXECUTIVE = "Executive"
    SALES = "Sales"
    MARKETING = "Marketing"
    OPERATIONS = "Operations"
    TECHNOLOGY = "Technology"
    FINANCE = "Finance"
    HUMAN_RESOURCES = "Human Resources"
    UNKNOWN = "Unknown"


class Seniority(str, Enum):
    """Seniority level classification."""
    EXECUTIVE = "Executive"
    VP = "VP"
    DIRECTOR = "Director"
    HEAD = "Head"
    MANAGER = "Manager"
    STAFF = "Staff"
    UNKNOWN = "Unknown"


class LeadershipPage(BaseModel):
    """Discovered candidate leadership or team webpage."""
    url: str = Field(..., description="Absolute URL of candidate leadership/team page")
    title: str | None = Field(default=None, description="Page title tag or heading")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence rating for page relevance")
    source: str = Field(default="Navigation Menu", description="Discovery vector (e.g. Navigation, Footer, Path Match)")


class DecisionMaker(BaseModel):
    """Extracted and normalized Decision Maker person profile."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    full_name: str = Field(..., description="Extracted full name")
    first_name: str | None = Field(default=None, description="First name")
    last_name: str | None = Field(default=None, description="Last name")
    title: str = Field(..., description="Original raw job title")
    normalized_title: str = Field(..., description="Standardized job title")
    department: Department = Field(default=Department.UNKNOWN, description="Department classification")
    seniority: Seniority = Field(default=Seniority.UNKNOWN, description="Seniority level")
    email: str | None = Field(default=None, description="Public email address")
    phone: str | None = Field(default=None, description="Public phone number")
    linkedin_url: str | None = Field(default=None, description="LinkedIn profile URL")
    biography: str | None = Field(default=None, description="Person biography or summary")
    image: str | None = Field(default=None, description="Person avatar or profile image URL")
    source_url: str = Field(..., description="URL where person profile was extracted")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="Overall extraction & identity confidence score")
    priority: int = Field(default=50, ge=0, le=100, description="Outreach priority score (0-100)")


class DecisionMakerDiscoveryReport(BaseModel):
    """Consolidated report for Decision Maker Discovery Engine (Phase 04)."""
    domain: str = Field(..., description="Target business domain")
    discovered_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Discovery timestamp"
    )
    leadership_pages: list[LeadershipPage] = Field(default_factory=list, description="Discovered leadership/team pages")
    decision_makers: list[DecisionMaker] = Field(default_factory=list, description="Extracted & ranked decision makers")
    total_people_found: int = Field(default=0, description="Total count of decision makers found")
    execution_time_seconds: float = Field(default=0.0, description="Execution duration in seconds")
    is_successful: bool = Field(default=True, description="True if engine completed cleanly")
    notes: list[str] = Field(default_factory=list, description="Execution warnings or audit notes")
