# Project Milestone Backlog

## High-Level Milestones

- [x] **Milestone 0: Workspace Setup & Repository Blueprint**
  - Establish workspace folder layout
  - Create documentation blueprint
  - Initialize empty Python project structure and Git repository

- [x] **Milestone 1: Company Discovery & Target Ingestion**
  - Implement `DomainNormalizer` & domain validation
  - Implement `MetadataField[T]` confidence containers & `Company` entity
  - Implement `CompanyRepository` pattern (`SQLiteCompanyRepository`, `InMemoryCompanyRepository`)
  - Implement `IngestionService` (single & bulk CSV/JSON/TXT seed file ingestion)
  - Implement CLI subcommands (`discover ingest`, `discover load`, `discover list`)
  - Unit test suite (13/13 passing tests)

- [ ] **Milestone 2: Website & Asset Discovery**
  - Resilient async web crawler, sitemap parser, and robots.txt engine

- [ ] **Milestone 3: Public Contact Discovery**
  - Public email, phone, contact form, and social link extraction

- [ ] **Milestone 4: Data Enrichment**
  - Enrichment pipeline for firmographic metadata

- [ ] **Milestone 5: Marketing & Technical Audit**
  - SEO audit engine and tech stack detector

- [ ] **Milestone 6: AI-Powered Posture Analysis**
  - AI analysis module for value propositions and opportunity mapping

- [ ] **Milestone 7: Lead Opportunity Scoring**
  - Configurable scoring rules and priority tier matrix

- [ ] **Milestone 8: Multi-Format Export Engine**
  - Structured JSON, CSV, Excel, and SQLite report exporters

- [ ] **Milestone 9: Agency User Interface / Dashboard**
  - Terminal CLI and web dashboard interface

- [ ] **Milestone 10: Production Readiness & Hardening**
  - Performance optimization, deployment, and final release
