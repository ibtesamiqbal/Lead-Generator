# Project Milestone Backlog

## High-Level Milestones

- [x] **Milestone 0: Workspace Setup & Repository Blueprint**
  - Establish workspace folder layout
  - Create documentation blueprint
  - Initialize empty Python project structure and Git repository

- [x] **Milestone 1: Company Discovery & Target Ingestion (Phase 1)**
  - Implement `normalize_domain` & domain validation
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

- [x] **Milestone 4: Decision Maker Discovery & Email Verification (Phase 4)**
  - Leadership candidate page scanner & people extractor
  - Title normalizer, department & seniority tiering
  - Syntax verification, spam-trap domain filtering, zero-mailbox-ping validation

- [x] **Milestone 5: Company Enrichment & Business Intelligence (Phase 5)**
  - 30+ B2B industry classifier & business model detector
  - Employee range tiering, service detector, hiring & trust signals

- [x] **Milestone 6: Marketing Intelligence & AI Posture Analysis (Phase 6 & 7)**
  - Content asset detection, conversion funnel score, CTA extractor, marketing tech audit
  - Overall digital maturity scoring, executive summary generator, top strengths & weaknesses, service recommendation matrix, outreach angles

- [x] **Milestone 7: Lead Scoring Matrix & Prioritization (Phase 6)**
  - Configurable weighted scoring matrix, grade assignment (`A+` to `F`), priority tiers (`HOT`, `WARM`, `COLD`), reason codes

- [x] **Milestone 8: Multi-Format Export Engine & Persistence (Phase 9)**
  - `ReportSerializer`, `JSONExporter`, `CSVExporter`, `ExcelExporter` (with CSV fallback), `SQLiteExporter` (`ON CONFLICT DO UPDATE`), and `PostgresExporter` (with full DDL, parameterized UPSERT, resource safety)

- [x] **Milestone 9: Agency CLI Interface & Script Registration (Phase 8)**
  - Subcommands (`discover`, `enrich`, `export`, `config`, `version`) and registered `lead-intel` console script entry point

- [ ] **Milestone 10: Production Readiness & Hardening (Phase 10)**
  - Performance optimization, deployment, containerization, and final release
