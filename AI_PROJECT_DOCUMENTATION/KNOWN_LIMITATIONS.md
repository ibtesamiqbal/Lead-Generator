# Known Limitations & Public Boundaries

## Public Crawling Scope
- **Public Data Only**: The system processes publicly available web data and explicitly respects `robots.txt` disallow paths.
- **Bot Protection Boundaries**: Websites employing aggressive anti-bot challenges (CAPTCHAs/Cloudflare) will be logged as unreachable/blocked rather than bypassed.
- **JavaScript Rendering**: Static HTTP parsing will miss purely client-side rendered Single-Page Applications (SPAs) unless headless browser fallback is enabled in future phases.
