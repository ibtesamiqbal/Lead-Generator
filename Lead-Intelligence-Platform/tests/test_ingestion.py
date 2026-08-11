"""
Unit Tests for IngestionService and Bulk Target File Ingestion.
"""

import json
import pytest
from pathlib import Path
from src.database.repository import InMemoryCompanyRepository
from src.discovery.ingestion import IngestionService
from src.utils.exceptions import DuplicateDomainError, DiscoveryError


@pytest.fixture
def service():
    repo = InMemoryCompanyRepository()
    return IngestionService(repo)


def test_ingest_single_domain_success(service):
    """Test registering a single valid target domain."""
    company = service.ingest_single_domain(
        domain="sydneyroofingexperts.com.au",
        name="Sydney Roofing Experts",
        industry="Roofing"
    )
    assert company.domain == "sydneyroofingexperts.com.au"
    assert company.name.value == "Sydney Roofing Experts"
    assert service.repository.count() == 1


def test_ingest_duplicate_domain_fails(service):
    """Test that attempting to re-ingest an existing domain raises DuplicateDomainError."""
    service.ingest_single_domain(domain="ozroofing.com.au")
    with pytest.raises(DuplicateDomainError):
        service.ingest_single_domain(domain="https://www.ozroofing.com.au/about")


def test_ingest_txt_file(service, tmp_path: Path):
    """Test bulk ingestion from a text file containing domain strings."""
    txt_file = tmp_path / "domains.txt"
    txt_file.write_text("roofing1.com.au\nroofing2.com.au\n# comment line\nroofing1.com.au\n", encoding="utf-8")

    summary = service.ingest_file(txt_file)
    assert summary.total_processed == 3
    assert summary.added_count == 2
    assert summary.duplicate_count == 1
    assert service.repository.count() == 2


def test_ingest_csv_file(service, tmp_path: Path):
    """Test bulk ingestion from CSV file."""
    csv_file = tmp_path / "targets.csv"
    csv_content = (
        "domain,name,industry,city\n"
        "brisbaneroofing.com.au,Brisbane Roofing,Roofing,Brisbane\n"
        "goldcoastremovals.com.au,Gold Coast Removals,Removal Companies,Gold Coast\n"
    )
    csv_file.write_text(csv_content, encoding="utf-8")

    summary = service.ingest_file(csv_file)
    assert summary.total_processed == 2
    assert summary.added_count == 2
    assert service.repository.count() == 2


def test_ingest_json_file(service, tmp_path: Path):
    """Test bulk ingestion from JSON spec file."""
    json_file = tmp_path / "targets.json"
    data = [
        {"domain": "perthroofing.com.au", "name": "Perth Roofing"},
        {"domain": "adelaideremovals.com.au", "name": "Adelaide Removals"}
    ]
    json_file.write_text(json.dumps(data), encoding="utf-8")

    summary = service.ingest_file(json_file)
    assert summary.added_count == 2
    assert service.repository.count() == 2
