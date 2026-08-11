"""
Target Ingestion Service.
Parses domain lists, CSV target files, and JSON specs into normalized Company entities.
"""

import csv
import json
from pathlib import Path
from typing import TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.database.repository import CompanyRepository

from src.discovery.models import Company, MetadataField, TargetStatus
from src.discovery.normalizer import normalize_domain, InvalidDomainError
from src.logging.logger import logger
from src.utils.exceptions import DiscoveryError, DuplicateDomainError


class IngestionSummary(BaseModel):
    """Summary metrics of target ingestion operation."""
    total_processed: int = Field(default=0)
    added_count: int = Field(default=0)
    duplicate_count: int = Field(default=0)
    error_count: int = Field(default=0)
    errors: list[str] = Field(default_factory=list)


class IngestionService:
    """Service orchestrating target company discovery and list ingestion."""

    def __init__(self, repository: "CompanyRepository"):
        self.repository = repository

    def ingest_single_domain(
        self,
        domain: str,
        name: str | None = None,
        industry: str = "Roofing",
        country: str = "Australia",
        city: str | None = None
    ) -> Company:
        """
        Ingest and register a single target company domain.
        """
        clean_domain = normalize_domain(domain)

        existing = self.repository.get_by_domain(clean_domain)
        if existing:
            raise DuplicateDomainError(f"Target domain '{clean_domain}' already exists in storage.")

        business_name = name or clean_domain.capitalize().split(".")[0]

        company = Company(
            domain=clean_domain,
            name=MetadataField[str](value=business_name, confidence=1.0 if name else 0.5),
            website_url=MetadataField[str](value=f"https://{clean_domain}", confidence=1.0),
            industry=MetadataField[str](value=industry, confidence=1.0),
            country=MetadataField[str](value=country, confidence=1.0),
            city=MetadataField[str](value=city, confidence=1.0) if city else MetadataField[str](),
            status=TargetStatus.PENDING
        )

        return self.repository.add(company)

    def ingest_file(self, file_path: Path | str) -> IngestionSummary:
        """
        Ingests bulk targets from a CSV, JSON, or TXT file.
        """
        path = Path(file_path)
        if not path.exists():
            raise DiscoveryError(f"Target ingestion file '{path}' does not exist.")

        summary = IngestionSummary()

        if path.suffix.lower() == ".json":
            self._ingest_json(path, summary)
        elif path.suffix.lower() == ".csv":
            self._ingest_csv(path, summary)
        else:
            self._ingest_txt(path, summary)

        logger.info(
            f"Ingestion complete: {summary.added_count} added, "
            f"{summary.duplicate_count} skipped duplicates, {summary.error_count} errors."
        )
        return summary

    def _ingest_txt(self, path: Path, summary: IngestionSummary):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue
                summary.total_processed += 1
                try:
                    self.ingest_single_domain(raw)
                    summary.added_count += 1
                except DuplicateDomainError:
                    summary.duplicate_count += 1
                except Exception as err:
                    summary.error_count += 1
                    summary.errors.append(f"Line '{raw}': {err}")

    def _ingest_csv(self, path: Path, summary: IngestionSummary):
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                summary.total_processed += 1
                domain_val = row.get("domain") or row.get("website") or row.get("url")
                if not domain_val:
                    summary.error_count += 1
                    summary.errors.append(f"Row {summary.total_processed}: Missing domain column.")
                    continue
                try:
                    self.ingest_single_domain(
                        domain=domain_val,
                        name=row.get("name") or row.get("company"),
                        industry=row.get("industry", "Roofing"),
                        country=row.get("country", "Australia"),
                        city=row.get("city")
                    )
                    summary.added_count += 1
                except DuplicateDomainError:
                    summary.duplicate_count += 1
                except Exception as err:
                    summary.error_count += 1
                    summary.errors.append(f"Row '{domain_val}': {err}")

    def _ingest_json(self, path: Path, summary: IngestionSummary):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data if isinstance(data, list) else data.get("targets", [])

        for item in items:
            summary.total_processed += 1
            if isinstance(item, str):
                domain_val, name_val = item, None
            else:
                domain_val = item.get("domain") or item.get("website_url")
                name_val = item.get("name")

            if not domain_val:
                summary.error_count += 1
                summary.errors.append(f"Item {summary.total_processed}: Missing domain.")
                continue

            try:
                self.ingest_single_domain(
                    domain=domain_val,
                    name=name_val,
                    industry=item.get("industry", "Roofing") if isinstance(item, dict) else "Roofing",
                    country=item.get("country", "Australia") if isinstance(item, dict) else "Australia"
                )
                summary.added_count += 1
            except DuplicateDomainError:
                summary.duplicate_count += 1
            except Exception as err:
                summary.error_count += 1
                summary.errors.append(f"Domain '{domain_val}': {err}")
