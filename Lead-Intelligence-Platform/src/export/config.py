"""
Configuration for Phase 09 — Export, Storage & Integration Layer.
"""

from pathlib import Path
from pydantic import BaseModel, Field


class ExportConfig(BaseModel):
    """Configuration for export file locations, database connection strings, and batch chunk sizes."""
    output_directory: Path = Field(default_factory=lambda: Path("exports"))
    sqlite_db_path: Path = Field(default_factory=lambda: Path("exports/lead_intelligence.db"))
    postgres_uri: str = Field(default="postgresql://user:pass@localhost:5432/lead_db")
    batch_chunk_size: int = Field(default=50, ge=1, le=1000)
    pretty_json: bool = Field(default=True)
