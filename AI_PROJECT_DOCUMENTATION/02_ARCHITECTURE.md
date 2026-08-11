# System Architecture

## Architecture Pattern
The platform follows a clean, decoupled modular pipeline architecture using the `src` layout in Python:

```
Lead-Intelligence-Platform/
├── src/
│   ├── config/          # Pydantic Settings & Environment Management
│   ├── database/        # Storage Abstractions & Repositories
│   ├── crawler/         # Async HTTP Scraper Engine & Rate Limiting
│   ├── discovery/       # Company & Website Discovery Engine
│   ├── extractors/      # HTML, Meta, Contact & Social Extractor
│   ├── parsers/         # DOM, XML Sitemap & Robots.txt Parsers
│   ├── enrichment/      # Public Data Enrichment Engine
│   ├── analysis/        # SEO & Tech Stack Audit Engines
│   ├── lead_scoring/    # Opportunity Matrix & Lead Scoring Engine
│   ├── export/          # Multi-format Exporters (JSON, CSV, HTML, PDF)
│   ├── utils/           # Shared Helpers & Core Utilities
│   └── logging/         # Structured Logger Infrastructure
```

## Core Pipeline Flow
1. **Target Ingestion**: Domain or business targets provided via CLI / API.
2. **Web Discovery & Crawling**: Async crawler fetches main page, sitemap.xml, robots.txt, and contact pages.
3. **Data Extraction & Parsing**: Extracts title/meta tags, headings, technology fingerprints, and public contact info.
4. **Digital Posture Analysis**: SEO and Technology detection engines audit website marketing strengths and gaps.
5. **Opportunity Scoring & Recommendations**: Calculates weighted Lead Score (0-100), assigns priority grade, and maps pitchable services.
6. **Report Export**: Exporters format output into JSON, CSV, or executive HTML summary documents.
