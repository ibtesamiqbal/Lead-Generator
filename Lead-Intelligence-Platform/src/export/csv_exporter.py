"""
CSV Exporter (Phase 09).
Exports normalized flat CSV files with streaming support.
"""

import csv
import time
from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport
from src.export.exporter import BaseExporter
from src.export.models import ExportFormat, ExportSummaryReport
from src.export.validators import ExportValidator
from src.logging.logger import logger


class CSVExporter(BaseExporter):
    """Writes flattened enrichment records to a CSV file."""

    async def export(
        self,
        reports: list[CompanyEnrichmentReport],
        destination: Path | str
    ) -> ExportSummaryReport:
        """
        Exports reports into a flat CSV file.
        """
        start_time = time.perf_counter()
        dest_path = Path(destination)
        ExportValidator.ensure_output_directory(dest_path)

        deduped = ExportValidator.deduplicate_reports(reports)
        flat_records = [self.serializer.to_flat_record(r) for r in deduped]

        fieldnames = list(flat_records[0].model_dump().keys()) if flat_records else []

        try:
            with open(dest_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for rec in flat_records:
                    writer.writerow(rec.model_dump())

            elapsed = round(time.perf_counter() - start_time, 4)
            logger.info(f"CSV Export completed: {len(flat_records)} records -> '{dest_path}' in {elapsed}s")
            return ExportSummaryReport(
                format=ExportFormat.CSV,
                total_records=len(reports),
                exported_records=len(flat_records),
                destination_path=str(dest_path),
                duration_seconds=elapsed,
                is_successful=True
            )
        except Exception as err:
            logger.error(f"CSV Export failed for '{dest_path}': {err}")
            return ExportSummaryReport(
                format=ExportFormat.CSV,
                total_records=len(reports),
                failed_records=len(reports),
                destination_path=str(dest_path),
                is_successful=False,
                errors=[str(err)]
            )
