"""
Unit Tests for Repository Storage Drivers (InMemory & SQLite).
"""

import pytest
from pathlib import Path
from src.database.repository import InMemoryCompanyRepository, SQLiteCompanyRepository
from src.discovery.models import Company, MetadataField, TargetStatus
from src.utils.exceptions import DuplicateDomainError, RepositoryError


@pytest.fixture
def memory_repo():
    return InMemoryCompanyRepository()


@pytest.fixture
def sqlite_repo(tmp_path: Path):
    db_file = tmp_path / "test_leads.db"
    return SQLiteCompanyRepository(db_path=db_file)


def test_in_memory_repository_crud(memory_repo):
    """Test CRUD functionality of InMemoryCompanyRepository."""
    c1 = Company(domain="roofingone.com.au", name=MetadataField[str](value="Roofing One"))
    memory_repo.add(c1)

    assert memory_repo.count() == 1
    retrieved = memory_repo.get_by_domain("roofingone.com.au")
    assert retrieved is not None
    assert retrieved.name.value == "Roofing One"

    # Test duplicate prevention
    with pytest.raises(DuplicateDomainError):
        memory_repo.add(Company(domain="HTTPS://WWW.roofingone.com.au/"))

    # Test update
    c1.status = TargetStatus.ANALYZED
    memory_repo.update(c1)
    assert memory_repo.get_by_domain("roofingone.com.au").status == TargetStatus.ANALYZED


def test_sqlite_repository_crud(sqlite_repo):
    """Test CRUD functionality of SQLiteCompanyRepository."""
    c1 = Company(domain="quickremovals.com.au", name=MetadataField[str](value="Quick Removals"))
    sqlite_repo.add(c1)

    assert sqlite_repo.count() == 1
    retrieved = sqlite_repo.get_by_domain("quickremovals.com.au")
    assert retrieved is not None
    assert retrieved.name.value == "Quick Removals"

    # Test duplicate prevention
    with pytest.raises(DuplicateDomainError):
        sqlite_repo.add(Company(domain="quickremovals.com.au"))

    # Test listing and filtering
    c2 = Company(domain="apexroofing.com.au", status=TargetStatus.ANALYZED)
    sqlite_repo.add(c2)

    assert sqlite_repo.count() == 2
    pending = sqlite_repo.list_all(status=TargetStatus.PENDING)
    assert len(pending) == 1
    assert pending[0].domain == "quickremovals.com.au"
