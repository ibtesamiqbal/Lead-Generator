"""
Pydantic Data Models for Phase 09 — Export, Storage & Integration Layer.
Defines schemas for export formats, flat records, batch job configs, and export summary reports.
"""

from enum import Enum
from pydantic import BaseModel, Field


class ExportFormat(str, Enum):
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    SQLITE = "sqlite"
    POSTGRES = "postgres"


class FlatCompanyRecord(BaseModel):
    """Flattened 1-row company record representation for CSV/Excel/Database export."""
    domain: str
    company_title: str = ""
    cms_name: str = "Unknown"
    industry: str = "Other B2B"
    company_size_tier: str = "Small Business (11-50)"
    estimated_employees: str = "11-50"
    overall_lead_score: int = 0
    grade: str = "F"
    priority: str = "COLD"
    confidence: float = 0.0
    purchase_potential: str = "Unknown"
    sales_urgency: str = "Low"
    estimated_sales_value: str = "Low"
    target_contact_role: str = "Managing Director / Owner"
    decision_makers_count: int = 0
    top_decision_maker: str = "None"
    contact_emails: str = ""
    contact_phones: str = ""
    marketing_maturity: str = "Basic"
    marketing_score: int = 0
    primary_cta: str = "None"
    recommended_services: str = ""
    positive_signals: str = ""
    negative_signals: str = ""
    reason_codes: str = ""
    exported_at: str = ""


class ExportSummaryReport(BaseModel):
    """Export Audit Execution Report."""
    format: ExportFormat
    total_records: int = 0
    exported_records: int = 0
    failed_records: int = 0
    destination_path: str = ""
    duration_seconds: float = 0.0
    is_successful: bool = True
    errors: list[str] = Field(default_factory=list)
