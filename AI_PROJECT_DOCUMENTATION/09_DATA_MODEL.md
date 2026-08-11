# Data Model Specification

## Core Data Schema Entities
- **`Company`**: Name, domain, website URL, description, industry, discovered timestamp, status.
- **`ContactInfo`**: Public email addresses, phone numbers, contact forms, social profile links (LinkedIn, FB, X, IG, YouTube), physical address.
- **`SEOAudit`**: Title tag, meta description, heading structure (H1-H6), OpenGraph tags, favicon, sitemap, `robots.txt`, SSL, mobile viewport, overall SEO score.
- **`TechStack`**: Detected CMS, analytics tags (GA4, GTM, Meta Pixel), marketing automation tools, tech maturity score.
- **`LeadScore`**: Overall 0-100 score, letter grade (A-F), outreach priority tier (Hot, Warm, Moderate, Low, Skip), score breakdown.
- **`ServiceRecommendation`**: Agency service name, priority, pitch rationale, estimated value tier.
- **`LeadReport`**: Consolidated entity combining company, audits, scores, and recommendations.
