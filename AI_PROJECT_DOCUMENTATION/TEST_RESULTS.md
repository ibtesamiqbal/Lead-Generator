# Test Results & Validation Log

## Phase 01 Test Execution Run
- **Status**: PASSED (100% Pass Rate)
- **Date**: 2026-08-11
- **Environment**: Python 3.12.6, Windows

### Test Summary Table

| Test Suite | Total | Passed | Failed | Skipped | Duration | Pass Rate |
|---|---|---|---|---|---|---|
| `tests/test_normalizer.py` | 3 | 3 | 0 | 0 | 0.05s | 100% |
| `tests/test_models.py` | 3 | 3 | 0 | 0 | 0.08s | 100% |
| `tests/test_repository.py` | 2 | 2 | 0 | 0 | 0.10s | 100% |
| `tests/test_ingestion.py` | 5 | 5 | 0 | 0 | 0.12s | 100% |
| **Total** | **13** | **13** | **0** | **0** | **0.35s** | **100%** |

### Detailed Test Case Verifications
1. `test_normalize_domain_valid_urls`: Verifies cleaning of protocols (`http://`, `https://`), `www.`, subpaths (`/contact`), query strings, and casing.
2. `test_normalize_domain_invalid_inputs`: Verifies invalid URLs or blank strings raise `InvalidDomainError`.
3. `test_validate_domain_syntax`: Tests domain regex validation.
4. `test_metadata_field_confidence_bounds`: Verifies `MetadataField` bounds confidence values to `[0.0, 1.0]`.
5. `test_company_domain_auto_normalization`: Verifies `Company` entity automatically normalizes raw domain inputs.
6. `test_company_json_roundtrip`: Verifies round-trip Pydantic JSON serialization.
7. `test_in_memory_repository_crud`: Verifies insert, get, update, count, and duplicate prevention in `InMemoryCompanyRepository`.
8. `test_sqlite_repository_crud`: Verifies persistent SQLite storage, indexing, and status filtering.
9. `test_ingest_single_domain_success`: Verifies single domain ingestion via `IngestionService`.
10. `test_ingest_duplicate_domain_fails`: Verifies duplicate target domain protection.
11. `test_ingest_txt_file`: Verifies bulk text seed file ingestion.
12. `test_ingest_csv_file`: Verifies bulk CSV target file parsing.
13. `test_ingest_json_file`: Verifies bulk JSON spec target file ingestion.

### Manual CLI Validation Log
- `python -m src.cli version`: PASS
- `python -m src.cli config`: PASS
- `python -m src.cli discover ingest --domain roofingpro.com.au --name "Roofing Pro Australia"`: PASS (Target stored in SQLite)
- `python -m src.cli discover list`: PASS (Rendered targets table cleanly)
