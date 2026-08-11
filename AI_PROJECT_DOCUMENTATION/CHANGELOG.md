# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.0] - 2026-08-11

### Added
- **Phase 01: Company Discovery & Target Ingestion Module**:
  - `src.config.settings`: Pydantic settings for default country (`Australia`), industries (`Roofing`, `Removal Companies`), SQLite path, and confidence threshold.
  - `src.utils.exceptions`: Custom exception hierarchy (`DiscoveryError`, `InvalidDomainError`, `RepositoryError`, `DuplicateDomainError`).
  - `src.logging.logger`: Structured console logger with `rich` formatting.
  - `src.discovery.normalizer`: Domain normalizer stripping protocols, `www.`, subpaths, and validating RFC syntax via regex.
  - `src.discovery.models`: `MetadataField[T]` confidence container with `[0.0, 1.0]` bounds and source tracking; `Company` domain entity.
  - `src.database.repository`: `CompanyRepository` abstraction with `SQLiteCompanyRepository` and `InMemoryCompanyRepository` storage drivers.
  - `src.discovery.ingestion`: `IngestionService` supporting single domain ingestion and bulk CSV/JSON/TXT seed target file ingestion with deduplication.
  - `src.cli`: Interactive CLI supporting `discover ingest`, `discover load`, `discover list`, `config`, and `version` commands.
  - Unit test suite (`tests/test_normalizer.py`, `tests/test_models.py`, `tests/test_repository.py`, `tests/test_ingestion.py`): 13/13 passing tests.

## [v0.0.1] - 2026-08-11
- Workspace initialization & governance blueprint.
