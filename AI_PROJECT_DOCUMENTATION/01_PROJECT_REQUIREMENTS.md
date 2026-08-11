# Project Requirements

## Executive Overview
The Lead Intelligence Platform enables digital marketing agencies to automatically discover target B2B companies, collect public business information, analyze online marketing presence (SEO, tech stack, speed, social links, analytics tracking), score sales opportunity potential, map weaknesses to pitched agency services, and export executive reports.

## High-Level Capabilities
1. **Company & Website Discovery**: Identify targets via domain input or search queries.
2. **Public Data Collection**: Extract public email addresses, phone numbers, contact forms, social media links, physical address.
3. **Technical SEO Audit**: Analyze titles, meta descriptions, H1-H6 tags, OpenGraph, SSL, sitemap.xml, robots.txt.
4. **Technology Stack Detection**: Detect CMS (WordPress, Webflow, Shopify), Analytics (GA4, GTM, Meta Pixel), Marketing Automation (HubSpot, Mailchimp).
5. **Marketing Opportunity Identification**: Highlight missing tracking pixels, weak SEO, slow load speed, broken links, lack of SSL.
6. **Lead Opportunity Scoring**: Assign 0-100 score, letter grade (A-F), and sales priority tier based on agency opportunity potential.
7. **Service Recommendation Engine**: Map identified gaps directly to pitchable agency services (e.g. SEO Audit, GA4 Setup, Redesign).
8. **Structured Reporting & Exporters**: Generate JSON, CSV, and stylized HTML/PDF executive lead reports.

## Non-Functional Requirements
- **Reliability & Resilience**: Scraper failures or blocked domains must never crash the pipeline.
- **Compliance**: Respect `robots.txt` disallows and domain request rate limits.
- **Maintainability**: Clean modular Python architecture with Pydantic type safety.
