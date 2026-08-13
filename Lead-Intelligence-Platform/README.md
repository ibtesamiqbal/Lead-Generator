# Lead Intelligence Platform (v0.3.0)

## Purpose
The Lead Intelligence Platform is an enterprise-grade solution designed for digital marketing agencies to identify high-quality target businesses, collect public business profile information, audit online digital marketing presence (SEO, tech stack, site performance, analytics tracking), calculate lead opportunity scores, and export structured lead reports.

## Installation & CLI Setup

```bash
# Install package and lead-intel CLI executable
pip install .
```

### CLI Command Options (`lead-intel` / `python -m src.cli`):
```bash
# Check version & environment configuration
lead-intel version
lead-intel config

# Ingest and list target companies
lead-intel discover ingest -d roofingpro.com.au -n "Roofing Specialists" -i Roofing -c Australia
lead-intel discover list

# Run enrichment pipeline
lead-intel enrich --domain roofingpro.com.au

# Export enriched reports to JSON, CSV, Excel, SQLite, or PostgreSQL
lead-intel export --domain roofingpro.com.au --format json
lead-intel export --domain roofingpro.com.au --format postgres --output "postgresql://user:pass@localhost:5432/lead_db"
```

## Project Layout (`src` Layout)
```
src/
├── __init__.py               # Package metadata (__version__ = "0.3.0")
├── cli.py                    # Agency CLI application (`lead-intel`)
├── config/                   # Application configuration & Pydantic settings
├── database/                 # Storage repositories & SQLite persistence
├── discovery/                # Target discovery & domain normalization
├── contact_discovery/        # Email, phone, address, & operating hours extraction
├── decision_maker/           # Executive discovery, people extraction, & title normalization
├── business_intelligence/    # Industry classification, firmographics, & service detection
├── marketing_intelligence/   # Conversion funnels, CTAs, & marketing tech auditing
├── ai_insights/              # Digital maturity, executive summary, & opportunity mapping
├── lead_scoring/             # Opportunity matrix & weighted lead scoring
├── enrichment/               # Master enrichment pipeline & technical analyzers
├── export/                   # Exporters (JSON, CSV, Excel, SQLite, PostgreSQL)
├── utils/                    # Shared utilities & exceptions
└── logging/                  # Structured logging
```

## PostgreSQL Export Support
The platform provides production-ready PostgreSQL persistence via `PostgresExporter` with automatic schema creation (`CREATE TABLE IF NOT EXISTS lead_records`), parameterized UPSERT execution (`INSERT INTO ... ON CONFLICT (domain) DO UPDATE`), resource closing, and graceful fallback when `psycopg2` is not present or PostgreSQL is unreachable.

## Testing & Quality Assurance
Run the automated test suite (189 unit & integration tests):
```bash
pytest
```
