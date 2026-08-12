# Phase 06 — Marketing Intelligence

## Overview

Phase 06 analyzes a company's digital marketing maturity using publicly available website content and metadata. It enriches each company with structured marketing intelligence that can later support AI recommendations, lead scoring, and sales outreach.

This phase consumes outputs from:

* Phase 01 — Company Discovery
* Phase 02 — Website Intelligence
* Phase 03 — Contact Discovery
* Phase 04 — Decision Maker Discovery
* Phase 05 — Business Intelligence

No previous phase should be modified.

---

# Objectives

Automatically evaluate:

* Marketing maturity
* SEO quality
* Content marketing
* Blog activity
* Social media presence
* Calls-to-action (CTAs)
* Lead generation assets
* Conversion optimization
* Brand consistency
* Customer engagement signals

---

# Expected Output

```json
{
  "marketing_intelligence": {
    "marketing_maturity": {
      "level": "Intermediate",
      "score": 74,
      "confidence": 0.89
    },
    "seo": {
      "title_quality": true,
      "meta_description": true,
      "structured_data": true,
      "internal_linking": "Good"
    },
    "content": {
      "blog_present": true,
      "latest_post_days": 12,
      "resources": [
        "Case Studies",
        "Guides",
        "Whitepapers"
      ]
    },
    "social": {
      "facebook": true,
      "linkedin": true,
      "instagram": false,
      "youtube": true
    },
    "conversion": {
      "contact_form": true,
      "newsletter": false,
      "live_chat": true,
      "quote_request": true,
      "booking": false
    },
    "cta": {
      "primary": "Request a Quote",
      "secondary": [
        "Book Consultation",
        "Call Now"
      ]
    },
    "analytics": {
      "ga4": true,
      "gtm": true,
      "meta_pixel": false,
      "linkedin_insight_tag": false
    },
    "overall_score": 78
  }
}
```

---

# Modules

## 1. Marketing Maturity Analyzer

Estimate overall digital marketing maturity using multiple weighted signals.

Levels:

* Basic
* Developing
* Intermediate
* Advanced
* Enterprise

---

## 2. SEO Intelligence

Evaluate:

* Title quality
* Meta descriptions
* Canonical tags
* Structured data
* Heading hierarchy
* Internal linking
* Image ALT usage
* Robots.txt
* XML sitemap

Reuse existing SEO outputs where possible instead of duplicating work.

---

## 3. Content Intelligence

Detect:

* Blog/news section
* Resource center
* Case studies
* Whitepapers
* Guides
* Videos
* FAQs

Estimate content freshness when dates are available.

---

## 4. Social Presence

Identify and normalize official links for:

* LinkedIn
* Facebook
* Instagram
* X
* YouTube
* TikTok

Measure completeness of social presence.

---

## 5. Conversion Optimization

Detect:

* Contact forms
* Quote request forms
* Demo requests
* Booking systems
* Newsletter signup
* Live chat widgets
* Downloadable assets

---

## 6. CTA Analysis

Identify prominent calls-to-action such as:

* Request a Quote
* Book Now
* Contact Us
* Schedule a Demo
* Free Trial
* Get Started

Rank CTAs by prominence.

---

## 7. Marketing Technology Detection

Identify technologies including:

* Google Analytics 4
* Google Tag Manager
* Meta Pixel
* LinkedIn Insight Tag
* HubSpot
* Hotjar
* Microsoft Clarity
* Common marketing automation tools

Leverage existing technology detection where possible.

---

# Folder Structure

```text
src/
└── marketing_intelligence/
    ├── models.py
    ├── maturity.py
    ├── seo.py
    ├── content.py
    ├── social.py
    ├── conversion.py
    ├── cta.py
    ├── marketing_tech.py
    ├── engine.py
    └── validators.py
```

---

# Coding Standards

* Python 3.12+
* Async-first architecture
* Pydantic models
* SOLID principles
* Strong typing
* Structured logging
* Comprehensive unit and integration tests
* Reuse outputs from previous phases wherever possible
* Avoid duplicate crawling or analysis

---

# Deliverables

The completed phase must:

* Integrate into the enrichment pipeline.
* Extend the company enrichment report with a `marketing_intelligence` section.
* Update the CLI to display a concise Marketing Intelligence summary.
* Include comprehensive unit, integration, and regression tests.
* Preserve compatibility with Phases 01–05.
* Be production-ready for use by AI Insights and Lead Scoring.
