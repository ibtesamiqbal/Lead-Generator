# Security & Compliance Guidelines

## Principles
1. **Zero Secrets in Code**: Never hardcode API keys, credentials, or tokens in source code or documentation. Use `.env`.
2. **Public Data Compliance**: Collect only publicly accessible business data. Respect `robots.txt` rules and rate limits.
3. **Input Sanitization**: Validate and sanitize all target URLs and inputs before processing to prevent SSRF or command injection.
