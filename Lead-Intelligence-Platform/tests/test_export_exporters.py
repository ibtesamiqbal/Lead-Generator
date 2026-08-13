"""
Unit tests for Phase 09 Exporters (CSV, Excel, JSON, SQLite, PostgreSQL).
"""

import json
import sqlite3
import pytest
from pathlib import Path

from src.enrichment.models import CompanyEnrichmentReport, FetchResult
from src.export import (
    CSVExporter,
    ExcelExporter,
    ExportFormat,
    JSONExporter,
    PostgresExporter,
    SQLiteExporter,
)


def _dummy_fetch(url: str = "https://example.com") -> FetchResult:
    return FetchResult(url=url, status_code=200, is_success=True)


@pytest.mark.anyio
async def test_csv_exporter(tmp_path: Path):
    dest = tmp_path / "test_export.csv"
    exporter = CSVExporter()
    reports = [CompanyEnrichmentReport(domain="testcsv.com", fetch_result=_dummy_fetch())]

    summary = await exporter.export(reports, dest)
    assert summary.is_successful is True
    assert summary.exported_records == 1
    assert dest.exists()


@pytest.mark.anyio
async def test_excel_exporter(tmp_path: Path):
    dest = tmp_path / "test_export.xlsx"
    exporter = ExcelExporter()
    reports = [CompanyEnrichmentReport(domain="testexcel.com", fetch_result=_dummy_fetch())]

    summary = await exporter.export(reports, dest)
    assert summary.is_successful is True
    assert summary.exported_records == 1
    assert dest.exists()


@pytest.mark.anyio
async def test_json_exporter(tmp_path: Path):
    dest = tmp_path / "test_export.json"
    exporter = JSONExporter(pretty=True)
    reports = [CompanyEnrichmentReport(domain="testjson.com", fetch_result=_dummy_fetch())]

    summary = await exporter.export(reports, dest)
    assert summary.is_successful is True
    assert dest.exists()

    with open(dest, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["domain"] == "testjson.com"


@pytest.mark.anyio
async def test_sqlite_exporter(tmp_path: Path):
    dest = tmp_path / "test_export.db"
    exporter = SQLiteExporter()
    reports = [CompanyEnrichmentReport(domain="testsqlite.com", fetch_result=_dummy_fetch())]

    summary = await exporter.export(reports, dest)
    assert summary.is_successful is True
    assert dest.exists()

    conn = sqlite3.connect(dest)
    cursor = conn.cursor()
    cursor.execute("SELECT domain FROM lead_records WHERE domain='testsqlite.com'")
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "testsqlite.com"


@pytest.mark.anyio
async def test_postgres_exporter():
    exporter = PostgresExporter()
    reports = [CompanyEnrichmentReport(domain="testpg.com", fetch_result=_dummy_fetch())]

    summary = await exporter.export(reports)
    assert summary.is_successful is True
    assert summary.format == ExportFormat.POSTGRES
    assert summary.exported_records == 1


@pytest.mark.anyio
async def test_postgres_exporter_with_custom_uri():
    exporter = PostgresExporter(connection_uri="postgresql://user:pass@invalid_host:5432/db")
    reports = [CompanyEnrichmentReport(domain="testpg_custom.com", fetch_result=_dummy_fetch())]

    summary = await exporter.export(reports)
    assert summary.is_successful is True
    assert summary.format == ExportFormat.POSTGRES
    assert summary.exported_records == 1

