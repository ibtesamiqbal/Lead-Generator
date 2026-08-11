# PHASE 03 – Contact Discovery Engine

---

## Objective

Implement a production-ready Contact Discovery Engine that discovers, validates, normalizes, and stores publicly available business contact information for companies identified during previous phases.

The Contact Discovery Engine extends the Website Intelligence Engine.

It must never bypass authentication, execute JavaScript, or collect private or protected information.

Only publicly accessible information may be processed.

---

# Current Project Status

Completed:

- Phase 01 – Company Discovery
- Phase 02 – Website Intelligence & Technical Intelligence

This phase must build on the existing enrichment pipeline.

Do not duplicate functionality implemented during previous phases.

---

# Functional Requirements

## Contact Discovery

Discover and normalize:

- Public email addresses
- Public phone numbers
- Mobile numbers
- Landline numbers
- Toll-free numbers
- Contact page URLs
- About page URLs
- Team page URLs
- Career page URLs
- Support page URLs
- Quote request pages

Every discovered contact must include:

- source URL
- confidence level
- discovery method
- validation status

---

## Email Intelligence

Extract emails from:

- homepage
- contact pages
- about pages
- footer
- header

Normalize addresses.

Remove duplicates.

Ignore obvious spam traps.

Classify emails where possible:

- General
- Sales
- Support
- Careers
- Marketing
- Accounts
- Owner
- Unknown

Validate syntax only.

Do not verify mailbox existence.

---

## Phone Intelligence

Extract:

- Australian phone numbers
- International phone numbers
- Mobile numbers
- Toll-free numbers

Normalize to E.164 where possible.

Classify number type.

Remove duplicates.

---

## Contact Page Discovery

Locate pages including:

- Contact
- About
- Team
- Staff
- Quote
- Estimate
- Request Quote
- Support
- Careers

Avoid crawling unrelated pages.

Respect configured crawl limits.

---

## Address Intelligence

Extract publicly available addresses.

Identify:

- Street
- City
- State
- Postal Code
- Country

Normalize formatting.

---

## Social Profile Validation

Validate previously discovered social profiles.

Identify:

- Broken profiles
- Redirected profiles
- Duplicate profiles

Record validation status.

---

## Business Hours

Extract published opening hours when available.

Normalize into structured format.

---

## Contact Confidence

Assign confidence levels.

HIGH

MEDIUM

LOW

Confidence should consider:

- source page
- validation
- duplication
- formatting quality

---

# Pipeline Integration

Extend the existing enrichment pipeline.

Pipeline:

Website Intelligence

↓

Technical Intelligence

↓

Contact Discovery

↓

Unified Company Profile

Each module must execute independently.

Failures must never terminate the pipeline.

---

# Data Models

Create strongly typed Pydantic models.

Suggested models:

- ContactEmail
- ContactPhone
- BusinessAddress
- BusinessHours
- ContactPage
- ContactDiscoveryReport

Reuse existing models wherever possible.

---

# Database

Extend storage to support:

- multiple emails
- multiple phones
- multiple addresses
- confidence values
- validation status
- discovery timestamps

---

# CLI

Extend CLI commands to expose contact discovery results.

Maintain backward compatibility.

---

# Testing

Requirements:

- Unit tests
- Mocked HTTP
- Mocked HTML
- No live internet access
- High coverage
- Deterministic execution

---

# Performance

Support batch processing.

Reuse parsed HTML.

Avoid duplicate HTTP requests.

Minimize memory usage.

Support asynchronous execution.

---

# Security

Only public information.

No authentication bypass.

No browser automation.

No penetration testing.

No mailbox verification.

Respect robots-related responses where applicable.

---

# Documentation

Update:

- PROJECT_STATUS.md
- TODO.md
- CHANGELOG.md
- TEST_RESULTS.md

Document all architectural decisions.

---

# Acceptance Criteria

This phase is complete when:

✓ Contact Discovery Engine is implemented.

✓ Contact validation is implemented.

✓ Contact normalization is implemented.

✓ Pipeline integration is complete.

✓ Unit tests pass.

✓ Existing tests pass.

✓ Documentation is updated.

✓ Changelog is updated.

✓ Project status reflects completion.

✓ Implementation is production-ready.
