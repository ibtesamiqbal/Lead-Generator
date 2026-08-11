# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.1] - 2026-08-11

### Fixed
- **Issue 1 – HTML Title Extraction**:
  - `src.enrichment.fetcher`: Dynamically configure `Accept-Encoding` header (`gzip, deflate`) based on `brotli` module availability to prevent unhandled compressed Brotli binary payloads.
  - `src.enrichment.parser`: Updated `HTMLParserDocument.get_title()` to use `self.soup.title.get_text(strip=True)` instead of `tag.string` so `<title>` tags containing comments or child tags are parsed cleanly.
  - `src.enrichment.metadata`: Added fallback to `og:title`, `twitter:title`, or `<h1 >` when `<title>` tag is absent or empty.
- **Issue 2 – Phone Number Extraction & Normalization Consistency**:
  - `src.utils.phone_normalizer`: Created shared `PhoneNormalizer` utility providing uniform validation and E.164 normalization for Australian landline/mobile/toll-free and valid international phone numbers. Rejects invalid digit strings.
  - `src.enrichment.contact_extractor` & `src.contact_discovery.phone_finder`: Refactored both modules to consume the shared `PhoneNormalizer` engine, ensuring 100% consistent phone normalization across Website Intelligence and Contact Discovery.

## [v0.3.0] - 2026-08-11

### Added
- **Phase 03: Contact Discovery Engine**:
  - `src.contact_discovery.models`: Schemas (`ContactEmail`, `ContactPhone`, `BusinessAddress`, `BusinessHours`, `ContactPage`, `SocialProfileValidation`, `ConfidenceLevel`, `EmailCategory`, `PhoneCategory`, `ContactPageCategory`, `ContactDiscoveryReport`).
  - `src.contact_discovery.email_finder`: `EmailFinder` for email extraction, classification (`General`, `Sales`, `Support`, `Careers`, `Accounts`, `Owner`), syntax validation, and spam trap domain filtering (`example.com`, `sentry.io`, image extensions). Zero mailbox pinging.
  - `src.contact_discovery.phone_finder`: `PhoneFinder` for Australian landline/mobile/toll-free and international numbers with E.164 normalization (`+612...`, `+614...`) and type classification (`Landline`, `Mobile`, `TollFree`).
  - `src.contact_discovery.page_finder`: `ContactPageFinder` locating secondary contact page URLs (`Contact`, `About`, `Team`, `Support`, `Careers`, `Quote`).
  - `src.contact_discovery.address_finder`: `AddressFinder` extracting Australian street addresses, city, state, postal code, and country.
  - `src.contact_discovery.hours_finder`: `BusinessHoursFinder` parsing operating schedule text into structured days/hours.
  - `src.contact_discovery.social_validator`: `SocialProfileValidator` inspecting social links for valid format, duplicate handles, and query redirects.
  - `src.contact_discovery.discovery_engine`: `ContactDiscoveryEngine` orchestrating primary & secondary contact page crawling and consolidating reports.
  - `src.enrichment.enrichment_pipeline`: Integrated `ContactDiscoveryEngine` into master enrichment workflow.
  - `src.cli`: Updated `enrich --domain roofingpro.com.au` CLI output to display contact emails, E.164 phones, and physical addresses.
  - Unit test suite (`tests/test_email_finder.py` through `tests/test_contact_discovery_engine.py`): 54/54 passing unit tests with 100% mocked HTTP transport.

## [v0.2.0] - 2026-08-11
- Phase 2: Website & Deep Technical Intelligence Engine.

## [v0.1.0] - 2026-08-11
- Phase 01: Company Discovery & Target Ingestion Module.

## [v0.0.1] - 2026-08-11
- Workspace initialization & governance blueprint.
