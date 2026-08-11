# Testing Strategy

## Strategy & Principles
1. **Unit Testing**: Pytest for isolated domain model validation, parsers, scoring calculations, and exporter formats.
2. **Integration Testing**: Async HTTP mock server tests verifying scraper retries, rate limiting, and exception boundaries.
3. **Validation Gates**: Every phase requires 100% passing tests before transitioning to the next phase.
4. **Test Log Documentation**: Results recorded in `TEST_RESULTS.md`.
