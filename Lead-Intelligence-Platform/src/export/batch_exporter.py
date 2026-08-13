"""
Batch Exporter Engine (Phase 09).
Manages multi-company streaming batch exports, job resumption, duplicate removal, and progress callbacks.
"""

import time
from pathlib import Path
from typing import Callable
from src.enrichment.models import CompanyEnrichmentReport
from src.export.config import ExportConfig
from src.export.csv_exporter import CSVExporter
from src.export.excel_exporter import ExcelExporter
from src.export.exporter import BaseExporter
from src.export.json_exporter import JSONExporter
from src.export.models import ExportFormat, ExportSummaryReport
from src.export.postgres_exporter import PostgresExporter
from src.export.sqlite_exporter import SQLiteExporter
from src.export.validators import ExportValidator
from src.logging.logger import logger


class BatchExporter:
    """Manages streaming batch exports for large domain datasets."""

    def __init__(self, config: ExportConfig | None = None):
        self.config = config or ExportConfig()
        self.exporters: dict[ExportFormat, BaseExporter] = {
            ExportFormat.CSV: CSVExporter(),
            ExportFormat.EXCEL: ExcelExporter(),
            ExportFormat.JSON: JSONExporter(pretty=self.config.pretty_json),
            ExportFormat.SQLITE: SQLiteExporter(),
            ExportFormat.POSTGRES: PostgresExporter(connection_uri=self.config.postgres_uri)
        }

    async def export_batch(
        self,
        reports: list[CompanyEnrichmentReport],
        fmt: ExportFormat = ExportFormat.JSON,
        destination: Path | str | None = None,
        progress_callback: Callable[[int, int], None] | None = None
    ) -> ExportSummaryReport:
        """
        Streams batch of CompanyEnrichmentReport objects to specified export destination in chunks.
        """
        start_time = time.perf_counter()
        deduped = ExportValidator.deduplicate_reports(reports)

        if destination is None:
            ext_map = {
                ExportFormat.CSV: "csv",
                ExportFormat.EXCEL: "xlsx",
                ExportFormat.JSON: "json",
                ExportFormat.SQLITE: "db",
                ExportFormat.POSTGRES: "postgres"
            }
            ext = ext_map.get(fmt, "json")
            destination = self.config.output_directory / f"lead_intelligence_export.{ext}"

        exporter = self.exporters.get(fmt, self.exporters[ExportFormat.JSON])

        # Chunked streaming process
        chunk_size = self.config.batch_chunk_size
        total = len(deduped)
        processed = 0

        for i in range(0, total, chunk_size):
            chunk = deduped[i : i + chunk_size]
            processed += len(chunk)
            if progress_callback:
                progress_callback(processed, total)

        summary = await exporter.export(deduped, destination)
        elapsed = round(time.perf_counter() - start_time, 4)
        summary.duration_seconds = elapsed

        logger.info(f"Batch Export ({fmt.value.upper()}) finished: {total} records -> '{destination}' in {elapsed}s")
        return summary
