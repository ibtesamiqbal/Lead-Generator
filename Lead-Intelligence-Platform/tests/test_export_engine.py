"""
Integration and Batch Streaming tests for ExportEngine & BatchExporter (Phase 09).
"""

import pytest
from pathlib import Path

from src.enrichment.models import CompanyEnrichmentReport, FetchResult
from src.export import ExportConfig, ExportEngine, ExportFormat


def _dummy_fetch(url: str = "https://example.com") -> FetchResult:
    return FetchResult(url=url, status_code=200, is_success=True)


@pytest.mark.anyio
async def test_export_engine_single_report(tmp_path: Path):
    dest = tmp_path / "single_export.json"
    engine = ExportEngine()
    report = CompanyEnrichmentReport(domain="single.com", fetch_result=_dummy_fetch("https://single.com"))

    summary = await engine.export_report(report, fmt=ExportFormat.JSON, destination=dest)
    assert summary.is_successful is True
    assert summary.exported_records == 1
    assert dest.exists()


@pytest.mark.anyio
async def test_batch_exporter_streaming(tmp_path: Path):
    dest = tmp_path / "batch_export.csv"
    cfg = ExportConfig(output_directory=tmp_path, batch_chunk_size=5)
    engine = ExportEngine(config=cfg)

    reports = [CompanyEnrichmentReport(domain=f"domain{i}.com", fetch_result=_dummy_fetch()) for i in range(15)]
    progress_count = 0

    def on_progress(proc: int, tot: int):
        nonlocal progress_count
        progress_count += 1

    summary = await engine.batch_exporter.export_batch(
        reports=reports,
        fmt=ExportFormat.CSV,
        destination=dest,
        progress_callback=on_progress
    )

    assert summary.is_successful is True
    assert summary.exported_records == 15
    assert progress_count >= 3
    assert dest.exists()
