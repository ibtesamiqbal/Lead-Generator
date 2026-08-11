"""
Discovery Module Data Schemas.
Implements MetadataField with confidence ratings and Company domain entity.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Generic, TypeVar
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator

from src.discovery.normalizer import normalize_domain

T = TypeVar("T")


class TargetStatus(str, Enum):
    """Discovery and audit target processing status."""
    PENDING = "pending"
    ANALYZED = "analyzed"
    UNREACHABLE = "unreachable"
    PARTIAL = "partial"
    FAILED = "failed"


class MetadataField(BaseModel, Generic[T]):
    """Generic container for extracted attributes with confidence scoring and source tracing."""
    value: T | None = Field(default=None, description="Extracted value")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    source: str | None = Field(default=None, description="Source URL or extraction method")
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of field extraction/update"
    )

    @field_validator("confidence", mode="before")
    @classmethod
    def clamp_confidence(cls, v: float) -> float:
        """Ensure confidence stays strictly bounded in [0.0, 1.0]."""
        try:
            val = float(v)
            return max(0.0, min(1.0, val))
        except (ValueError, TypeError):
            return 1.0


class Company(BaseModel):
    """Core Company Profile Entity."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique company ID")
    domain: str = Field(..., description="Normalized target domain string (e.g. roofingpro.com.au)")
    name: MetadataField[str] = Field(
        default_factory=lambda: MetadataField[str](value="Unknown Business", confidence=0.0),
        description="Discovered business name"
    )
    website_url: MetadataField[str] = Field(
        default_factory=lambda: MetadataField[str](),
        description="Canonical website URL"
    )
    industry: MetadataField[str] = Field(
        default_factory=lambda: MetadataField[str](value="Roofing"),
        description="Target industry sector"
    )
    country: MetadataField[str] = Field(
        default_factory=lambda: MetadataField[str](value="Australia"),
        description="Country location"
    )
    state: MetadataField[str] = Field(default_factory=lambda: MetadataField[str]())
    city: MetadataField[str] = Field(default_factory=lambda: MetadataField[str]())
    address: MetadataField[str] = Field(default_factory=lambda: MetadataField[str]())

    status: TargetStatus = Field(default=TargetStatus.PENDING, description="Current analysis status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Company record creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Company record last update timestamp"
    )

    @field_validator("domain")
    @classmethod
    def validate_and_clean_domain(cls, v: str) -> str:
        """Enforce domain normalization on instance creation."""
        return normalize_domain(v)
