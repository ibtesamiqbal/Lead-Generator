"""
JSON Exporter (Phase 09).
Exports nested CompanyEnrichmentReport objects as pretty or compact JSON files.
"""

import json
import time
from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport
from src.export.exporter import BaseExporter
from src.export.models import ExportFormat, ExportSummaryReport
from src.export.validators import ExportValidator
from src.logging.logger import logger


class JSONExporter(BaseExporter):
    """Writes nested enrichment reports to JSON files."""

    def __init__(self, pretty: bool = True):
        super().__init__()
        self.pretty = pretty

    async def export(
        self,
        reports: list[CompanyEnrichmentReport],
        destination: Path | str
    ) -> ExportSummaryReport:
        """
        Exports reports into nested JSON file.
        """
        start_time = time.perf_counter()
        dest_path = Path(destination)
        ExportValidator.ensure_output_directory(dest_path)

        deduped = ExportValidator.deduplicate_reports(reports)
        dicts = [self.serializer.to_dict(r) for r in deduped]

        try:
            indent = 2 if self.pretty else None
            with open(dest_path, mode="w", encoding="utf-8") as f:
                json.dump(dicts, f, indent=indent, default=str)

            elapsed = round(time.perf_counter() - start_time, 4)
            logger.info(f"JSON Export completed: {len(deduped)} records -> '{dest_path}' in {elapsed}s")
            return ExportSummaryReport(
                format=ExportFormat.JSON,
                total_records=len(reports),
                exported_records=len(deduped),
                destination_path=str(dest_path),
                duration_seconds=elapsed,
                is_successful=True
            )
        except Exception as err:
            logger.error(f"JSON Export failed for '{dest_path}': {err}")
            return ExportSummaryReport(
                format=ExportFormat.JSON,
                total_records=len(reports),
                failed_records=len(reports),
                destination_path=str(dest_path),
                is_successful=False,
                errors=[str(err)]
            )
