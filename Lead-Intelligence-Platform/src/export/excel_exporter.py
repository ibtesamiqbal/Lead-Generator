"""
Excel Exporter (Phase 09).
Exports multi-sheet XLSX workbooks using openpyxl when available, with clean fallback to CSV/TSV format.
"""

import csv
import time
from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport
from src.export.exporter import BaseExporter
from src.export.models import ExportFormat, ExportSummaryReport
from src.export.validators import ExportValidator
from src.logging.logger import logger


class ExcelExporter(BaseExporter):
    """Writes multi-sheet XLSX workbooks or clean tabular exports."""

    async def export(
        self,
        reports: list[CompanyEnrichmentReport],
        destination: Path | str
    ) -> ExportSummaryReport:
        """
        Exports reports into multi-sheet XLSX workbook or fallback CSV tabular file.
        """
        start_time = time.perf_counter()
        dest_path = Path(destination)
        ExportValidator.ensure_output_directory(dest_path)

        deduped = ExportValidator.deduplicate_reports(reports)

        try:
            try:
                import openpyxl
                wb = openpyxl.Workbook()

                # Sheet 1: Companies (Overview)
                ws_comp = wb.active
                ws_comp.title = "Companies"
                flat_recs = [self.serializer.to_flat_record(r) for r in deduped]

                if flat_recs:
                    headers = list(flat_recs[0].model_dump().keys())
                    ws_comp.append(headers)
                    for rec in flat_recs:
                        ws_comp.append(list(rec.model_dump().values()))

                # Sheet 2: Decision Makers
                ws_dms = wb.create_sheet(title="Decision Makers")
                ws_dms.append(["Domain", "Full Name", "Title", "Normalized Title", "Department", "Seniority", "Email", "Phone", "LinkedIn"])
                for r in deduped:
                    if r.decision_maker_discovery and r.decision_maker_discovery.decision_makers:
                        for dm in r.decision_maker_discovery.decision_makers:
                            ws_dms.append([r.domain, dm.full_name, dm.title, dm.normalized_title, dm.department.value, dm.seniority.value, dm.email or "", dm.phone or "", dm.linkedin_url or ""])

                wb.save(dest_path)
            except ImportError:
                # Fallback to standard CSV output when openpyxl is not installed
                flat_records = [self.serializer.to_flat_record(r) for r in deduped]
                fieldnames = list(flat_records[0].model_dump().keys()) if flat_records else []
                with open(dest_path, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for rec in flat_records:
                        writer.writerow(rec.model_dump())

            elapsed = round(time.perf_counter() - start_time, 4)
            logger.info(f"Excel/Tabular Export completed: {len(deduped)} records -> '{dest_path}' in {elapsed}s")
            return ExportSummaryReport(
                format=ExportFormat.EXCEL,
                total_records=len(reports),
                exported_records=len(deduped),
                destination_path=str(dest_path),
                duration_seconds=elapsed,
                is_successful=True
            )
        except Exception as err:
            logger.error(f"Excel Export failed for '{dest_path}': {err}")
            return ExportSummaryReport(
                format=ExportFormat.EXCEL,
                total_records=len(reports),
                failed_records=len(reports),
                destination_path=str(dest_path),
                is_successful=False,
                errors=[str(err)]
            )
