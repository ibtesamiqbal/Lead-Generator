"""
Repository Pattern Implementation for Company Data Storage.
Provides abstract interface with SQLite and In-Memory storage drivers.
"""

import json
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from src.config.settings import settings
from src.discovery.models import Company, TargetStatus
from src.utils.exceptions import RepositoryError, DuplicateDomainError


class CompanyRepository(ABC):
    """Abstract Base Repository Interface for Company objects."""

    @abstractmethod
    def add(self, company: Company) -> Company:
        """Insert a new company record. Raises DuplicateDomainError if domain exists."""
        pass

    @abstractmethod
    def get_by_domain(self, domain: str) -> Company | None:
        """Retrieve company by normalized domain."""
        pass

    @abstractmethod
    def get_by_id(self, company_id: str) -> Company | None:
        """Retrieve company by UUID."""
        pass

    @abstractmethod
    def list_all(self, status: TargetStatus | None = None) -> list[Company]:
        """List all company records, optionally filtered by status."""
        pass

    @abstractmethod
    def update(self, company: Company) -> Company:
        """Update an existing company record."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Return total count of stored companies."""
        pass


class InMemoryCompanyRepository(CompanyRepository):
    """In-Memory repository driver for testing and fast execution."""

    def __init__(self):
        self._by_id: dict[str, Company] = {}
        self._by_domain: dict[str, Company] = {}

    def add(self, company: Company) -> Company:
        if company.domain in self._by_domain:
            raise DuplicateDomainError(f"Company domain '{company.domain}' already exists.")
        self._by_id[company.id] = company
        self._by_domain[company.domain] = company
        return company

    def get_by_domain(self, domain: str) -> Company | None:
        return self._by_domain.get(domain.lower().strip())

    def get_by_id(self, company_id: str) -> Company | None:
        return self._by_id.get(company_id)

    def list_all(self, status: TargetStatus | None = None) -> list[Company]:
        companies = list(self._by_id.values())
        if status:
            return [c for c in companies if c.status == status]
        return companies

    def update(self, company: Company) -> Company:
        if company.id not in self._by_id:
            raise RepositoryError(f"Company ID '{company.id}' not found for update.")
        self._by_id[company.id] = company
        self._by_domain[company.domain] = company
        return company

    def count(self) -> int:
        return len(self._by_id)


class SQLiteCompanyRepository(CompanyRepository):
    """Production-grade SQLite Repository Driver."""

    def __init__(self, db_path: Path | str | None = None):
        self.db_path = Path(db_path or settings.database.sqlite_db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize database schema if table does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS companies (
            id TEXT PRIMARY KEY,
            domain TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            data_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_companies_domain ON companies(domain);
        CREATE INDEX IF NOT EXISTS idx_companies_status ON companies(status);
        """
        with self._get_connection() as conn:
            conn.executescript(query)

    def add(self, company: Company) -> Company:
        if self.get_by_domain(company.domain):
            raise DuplicateDomainError(f"Company domain '{company.domain}' already exists in SQLite.")

        query = """
        INSERT INTO companies (id, domain, status, data_json, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        data_json = company.model_dump_json()
        with self._get_connection() as conn:
            conn.execute(
                query,
                (
                    company.id,
                    company.domain,
                    company.status.value,
                    data_json,
                    company.created_at.isoformat(),
                    company.updated_at.isoformat(),
                ),
            )
            conn.commit()
        return company

    def get_by_domain(self, domain: str) -> Company | None:
        query = "SELECT data_json FROM companies WHERE domain = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (domain.lower().strip(),)).fetchone()
            if row:
                return Company.model_validate_json(row["data_json"])
        return None

    def get_by_id(self, company_id: str) -> Company | None:
        query = "SELECT data_json FROM companies WHERE id = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (company_id,)).fetchone()
            if row:
                return Company.model_validate_json(row["data_json"])
        return None

    def list_all(self, status: TargetStatus | None = None) -> list[Company]:
        if status:
            query = "SELECT data_json FROM companies WHERE status = ?"
            params = (status.value,)
        else:
            query = "SELECT data_json FROM companies"
            params = ()

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [Company.model_validate_json(row["data_json"]) for row in rows]

    def update(self, company: Company) -> Company:
        query = """
        UPDATE companies
        SET status = ?, data_json = ?, updated_at = ?
        WHERE id = ?
        """
        data_json = company.model_dump_json()
        with self._get_connection() as conn:
            cursor = conn.execute(
                query,
                (company.status.value, data_json, company.updated_at.isoformat(), company.id),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise RepositoryError(f"Company ID '{company.id}' not found for update.")
        return company

    def count(self) -> int:
        query = "SELECT COUNT(*) as total FROM companies"
        with self._get_connection() as conn:
            row = conn.execute(query).fetchone()
            return row["total"] if row else 0
