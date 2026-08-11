"""
Configuration management for Lead Intelligence Platform.
Uses Pydantic BaseSettings for environment variable reading and sensible defaults.
"""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscoverySettings(BaseSettings):
    """Target company discovery settings."""
    default_country: str = Field(default="Australia", description="Default target country location")
    default_industries: list[str] = Field(
        default_factory=lambda: ["Roofing", "Removal Companies"],
        description="Initial target industry sectors"
    )
    confidence_threshold: float = Field(
        default=0.5,
        description="Minimum confidence score threshold for extracted fields"
    )


class DatabaseSettings(BaseSettings):
    """Database storage settings."""
    sqlite_db_path: Path = Field(
        default=Path("data/lead_intelligence.db"),
        description="SQLite database storage filepath"
    )


class Settings(BaseSettings):
    """Master Application Settings."""
    model_config = SettingsConfigDict(
        env_prefix="LEAD_INTEL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    app_name: str = Field(default="Lead Intelligence Platform")
    environment: str = Field(default="development", description="development, staging, production")
    debug: bool = Field(default=False)

    discovery: DiscoverySettings = Field(default_factory=DiscoverySettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)


settings = Settings()
