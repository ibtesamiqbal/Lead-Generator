# Project Milestone Backlog

## High-Level Milestones

- [x] **Milestone 0: Workspace Setup & Repository Blueprint**
  - Establish workspace folder layout
  - Create documentation blueprint
  - Initialize empty Python project structure and Git repository

- [x] **Milestone 1: Company Discovery & Target Ingestion (Phase 1)**
  - Implement `DomainNormalizer` & domain validation
  - Implement `MetadataField[T]` confidence containers & `Company` entity
  - Implement `CompanyRepository` pattern (`SQLiteCompanyRepository`, `InMemoryCompanyRepository`)
  - Implement `IngestionService` (single & bulk CSV/JSON/TXT seed file ingestion)
  - Implement CLI subcommands (`discover ingest`, `discover load`, `discover list`)

- [x] **Milestone 2: Website & Technical Intelligence Engine (Phase 2)**
  - Resilient async HTTP client (`HTTPFetcher`) with session reuse & backoff retries
  - Safe HTML parser (`HTMLParserDocument`)
  - Full document metadata extractor (`WebsiteMetadata`)
  - Public contact extractor (`ContactIntelligence` with phone normalization)
  - Social media extractor (`SocialProfiles` for FB, IG, LinkedIn, X, YT, TikTok, Pinterest)
  - Multi-heuristic CMS detector (`CMSDetectionResult`)
  - `robots.txt` and `sitemap.xml` XML parsers
  - Technical Analyzers (SEO, Structured Data, Expanded Tech Stack, Performance, Accessibility, Link, Passive Security)

- [x] **Milestone 3: Contact Discovery Engine (Phase 3)**
  - Email intelligence (regex extraction, spam trap filter, syntax validation, classification)
  - Phone intelligence (Australian & international E.164 normalization, Landline/Mobile/TollFree classification)
  - Secondary page finder (Contact, About, Team, Support, Careers, Quote)
  - Physical address finder & business operating hours finder
  - Social profile validator (duplicate handle & redirect parameter detection)
  - Master `ContactDiscoveryEngine` & pipeline integration
  - Unit test suite (54/54 passing tests with 100% mocked HTTP transport)

- [ ] **Milestone 4: Data Enrichment**
  - Enrichment pipeline for firmographic metadata

- [ ] **Milestone 5: Marketing & Technical Audit**
  - On-page technical SEO audit engine and speed/security posture

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
