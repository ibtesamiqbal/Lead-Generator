"""
SQLite Exporter (Phase 09).
Creates normalized relational SQLite database tables with UPSERT semantics.
"""

import sqlite3
import time
from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport
from src.export.exporter import BaseExporter
from src.export.models import ExportFormat, ExportSummaryReport
from src.export.validators import ExportValidator
from src.logging.logger import logger


class SQLiteExporter(BaseExporter):
    """Persists flattened records into an SQLite database file."""

    async def export(
        self,
        reports: list[CompanyEnrichmentReport],
        destination: Path | str
    ) -> ExportSummaryReport:
        """
        Exports reports into relational SQLite database.
        """
        start_time = time.perf_counter()
        dest_path = Path(destination)
        ExportValidator.ensure_output_directory(dest_path)

        deduped = ExportValidator.deduplicate_reports(reports)
        flat_records = [self.serializer.to_flat_record(r) for r in deduped]

        try:
            conn = sqlite3.connect(dest_path)
            cursor = conn.cursor()

            # Create lead_records table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS lead_records (
                domain TEXT PRIMARY KEY,
                company_title TEXT,
                cms_name TEXT,
                industry TEXT,
                company_size_tier TEXT,
                estimated_employees TEXT,
                overall_lead_score INTEGER,
                grade TEXT,
                priority TEXT,
                confidence REAL,
                purchase_potential TEXT,
                sales_urgency TEXT,
                estimated_sales_value TEXT,
                target_contact_role TEXT,
                decision_makers_count INTEGER,
                top_decision_maker TEXT,
                contact_emails TEXT,
                contact_phones TEXT,
                marketing_maturity TEXT,
                marketing_score INTEGER,
                primary_cta TEXT,
                recommended_services TEXT,
                positive_signals TEXT,
                negative_signals TEXT,
                reason_codes TEXT,
                exported_at TEXT
            )
            """)

            for rec in flat_records:
                d = rec.model_dump()
                cursor.execute("""
                INSERT INTO lead_records (
                    domain, company_title, cms_name, industry, company_size_tier,
                    estimated_employees, overall_lead_score, grade, priority, confidence,
                    purchase_potential, sales_urgency, estimated_sales_value, target_contact_role,
                    decision_makers_count, top_decision_maker, contact_emails, contact_phones,
                    marketing_maturity, marketing_score, primary_cta, recommended_services,
                    positive_signals, negative_signals, reason_codes, exported_at
                ) VALUES (
                    :domain, :company_title, :cms_name, :industry, :company_size_tier,
                    :estimated_employees, :overall_lead_score, :grade, :priority, :confidence,
                    :purchase_potential, :sales_urgency, :estimated_sales_value, :target_contact_role,
                    :decision_makers_count, :top_decision_maker, :contact_emails, :contact_phones,
                    :marketing_maturity, :marketing_score, :primary_cta, :recommended_services,
                    :positive_signals, :negative_signals, :reason_codes, :exported_at
                ) ON CONFLICT(domain) DO UPDATE SET
                    company_title=excluded.company_title,
                    overall_lead_score=excluded.overall_lead_score,
                    grade=excluded.grade,
                    priority=excluded.priority,
                    exported_at=excluded.exported_at
                """, d)

            conn.commit()
            conn.close()

            elapsed = round(time.perf_counter() - start_time, 4)
            logger.info(f"SQLite Export completed: {len(flat_records)} records -> '{dest_path}' in {elapsed}s")
            return ExportSummaryReport(
                format=ExportFormat.SQLITE,
                total_records=len(reports),
                exported_records=len(flat_records),
                destination_path=str(dest_path),
                duration_seconds=elapsed,
                is_successful=True
            )
        except Exception as err:
            logger.error(f"SQLite Export failed for '{dest_path}': {err}")
            return ExportSummaryReport(
                format=ExportFormat.SQLITE,
                total_records=len(reports),
                failed_records=len(reports),
                destination_path=str(dest_path),
                is_successful=False,
                errors=[str(err)]
            )
