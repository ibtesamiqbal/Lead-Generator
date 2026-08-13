"""
Master Export Engine Orchestrator (Phase 09).
Coordinates serialization, format exporters, SQLite/PostgreSQL persistence, and batch processing.
"""

from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport
from src.export.batch_exporter import BatchExporter
from src.export.config import ExportConfig
from src.export.models import ExportFormat, ExportSummaryReport


class ExportEngine:
    """Master orchestrator for Phase 09 Export, Storage & Integration Layer."""

    def __init__(self, config: ExportConfig | None = None):
        self.config = config or ExportConfig()
        self.batch_exporter = BatchExporter(config=self.config)

    async def export_report(
        self,
        report: CompanyEnrichmentReport,
        fmt: ExportFormat = ExportFormat.JSON,
        destination: Path | str | None = None
    ) -> ExportSummaryReport:
        """
        Exports a single CompanyEnrichmentReport object.
        """
        return await self.batch_exporter.export_batch(
            reports=[report],
            fmt=fmt,
            destination=destination
        )

    async def export_reports(
        self,
        reports: list[CompanyEnrichmentReport],
        fmt: ExportFormat = ExportFormat.JSON,
        destination: Path | str | None = None
    ) -> ExportSummaryReport:
        """
        Exports a collection of CompanyEnrichmentReport objects.
        """
        return await self.batch_exporter.export_batch(
            reports=reports,
            fmt=fmt,
            destination=destination
        )
