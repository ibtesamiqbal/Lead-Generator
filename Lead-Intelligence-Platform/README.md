# Lead Intelligence Platform

## Purpose
The Lead Intelligence Platform is an enterprise-grade solution designed for digital marketing agencies to identify high-quality target businesses, collect public business profile information, audit online digital marketing presence (SEO, tech stack, site performance, analytics tracking), calculate lead opportunity scores, and export structured lead reports.

## Project Layout (`src` Layout)
```
src/
├── config/          # Application configuration settings
├── database/        # Storage repositories and database models
├── crawler/         # Resilient web crawler & HTTP client engine
├── discovery/       # Target discovery modules
├── extractors/      # HTML, contact info, and social metadata extractors
├── parsers/         # DOM, sitemap, and robots.txt parsers
├── enrichment/      # Public data enrichment services
├── analysis/        # Technical SEO & technology audit engines
├── lead_scoring/    # Opportunity matrix & lead scoring models
├── export/          # JSON, CSV, and HTML exporters
├── utils/           # Helper utilities
└── logging/         # Structured logger setup
```

## Development Workflow & Git Usage
- **Phase-Based Progress**: Features are implemented phase by phase.
- **Testing Requirements**: Each phase requires 100% test validation before completion.
- **Documentation**: All architectural updates are logged in `../AI_PROJECT_DOCUMENTATION/`.
