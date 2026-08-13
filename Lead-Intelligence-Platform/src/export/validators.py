"""
Validator & Deduplication Utilities for Export Layer.
"""

from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport


class ExportValidator:
    """Utilities for output path validation, domain deduplication, and export record checks."""

    @staticmethod
    def ensure_output_directory(path: Path) -> Path:
        """Ensures parent export directory exists."""
        if path.is_file() or path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def deduplicate_reports(reports: list[CompanyEnrichmentReport]) -> list[CompanyEnrichmentReport]:
        """Deduplicates enrichment reports by target domain keeping the latest."""
        seen: set[str] = set()
        deduped: list[CompanyEnrichmentReport] = []
        for r in reversed(reports):
            dom = r.domain.lower().strip()
            if dom not in seen:
                seen.add(dom)
                deduped.append(r)
        return list(reversed(deduped))
