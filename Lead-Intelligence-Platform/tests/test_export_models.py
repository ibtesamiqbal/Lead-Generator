"""
Unit tests for Phase 09 — Export Models, Config, Serializer & Validators.
"""

from src.enrichment.models import CompanyEnrichmentReport, FetchResult
from src.export import EnrichmentSerializer, ExportConfig, ExportFormat, ExportSummaryReport, ExportValidator, FlatCompanyRecord


def _dummy_fetch(url: str = "https://example.com") -> FetchResult:
    return FetchResult(url=url, status_code=200, is_success=True)


def test_export_config_defaults():
    cfg = ExportConfig()
    assert cfg.batch_chunk_size == 50
    assert cfg.pretty_json is True


def test_serializer_to_flat_record():
    serializer = EnrichmentSerializer()
    report = CompanyEnrichmentReport(domain="daikin.com.au", fetch_result=_dummy_fetch("https://daikin.com.au"))

    flat = serializer.to_flat_record(report)
    assert isinstance(flat, FlatCompanyRecord)
    assert flat.domain == "daikin.com.au"


def test_export_validator_deduplication():
    reports = [
        CompanyEnrichmentReport(domain="sitea.com", fetch_result=_dummy_fetch()),
        CompanyEnrichmentReport(domain="siteb.com", fetch_result=_dummy_fetch()),
        CompanyEnrichmentReport(domain="sitea.com", fetch_result=_dummy_fetch())
    ]
    deduped = ExportValidator.deduplicate_reports(reports)
    assert len(deduped) == 2
    assert deduped[0].domain == "siteb.com"
    assert deduped[1].domain == "sitea.com"
