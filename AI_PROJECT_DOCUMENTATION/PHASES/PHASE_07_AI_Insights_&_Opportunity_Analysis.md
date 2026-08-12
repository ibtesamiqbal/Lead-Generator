# Phase 07 — AI Insights & Opportunity Analysis

## Overview

Phase 07 transforms the structured outputs from Phases 01–06 into actionable business intelligence for sales teams.

Unlike previous phases, this phase does **not** perform new web scraping. It consumes the normalized enrichment data already produced by the platform and generates explainable AI-driven insights.

The goal is to answer:

* What kind of business is this?
* How digitally mature is it?
* What are its strengths?
* What weaknesses or gaps exist?
* Which services are most relevant to offer?
* What sales approach is likely to be most effective?
* Why should this lead be prioritized?

This phase prepares the platform for Phase 08 (Lead Scoring) by producing structured recommendations and confidence-based insights.

---

# Inputs

Consume the outputs from:

* Phase 01 — Company Discovery
* Phase 02 — Website Intelligence
* Phase 03 — Contact Discovery
* Phase 04 — Decision Maker Discovery
* Phase 05 — Business Intelligence
* Phase 06 — Marketing Intelligence

No additional crawling should occur.

---

# Objectives

Generate structured AI insights for:

* Executive business summary
* Digital maturity assessment
* Business strengths
* Business weaknesses
* Website opportunities
* SEO opportunities
* Marketing opportunities
* Sales opportunities
* Technology recommendations
* Outreach recommendations
* Risk assessment
* Overall AI confidence

---

# Expected Output

```json
{
  "ai_insights": {
    "executive_summary": "Established HVAC company serving commercial and residential customers with strong local presence but moderate digital maturity.",
    "digital_maturity": {
      "level": "Intermediate",
      "score": 73
    },
    "strengths": [
      "Strong service portfolio",
      "Multiple trust signals",
      "Well-optimized website"
    ],
    "weaknesses": [
      "No public executive contact information",
      "Limited conversion opportunities",
      "Weak content marketing"
    ],
    "opportunities": {
      "seo": [
        "Improve internal linking",
        "Expand local landing pages"
      ],
      "marketing": [
        "Publish case studies",
        "Launch newsletter"
      ],
      "sales": [
        "Offer CRM integration",
        "Recommend marketing automation"
      ]
    },
    "recommended_services": [
      "SEO Optimization",
      "Website Conversion Optimization",
      "Marketing Automation"
    ],
    "outreach_strategy": {
      "primary_contact": "Owner or Managing Director",
      "approach": "Consultative",
      "opening_angle": "Improve online lead generation and website conversion."
    },
    "risks": [
      "Estimated company size has medium confidence."
    ],
    "confidence": 0.91
  }
}
```

---

# Modules

## 1. Executive Summary Generator

Generate a concise business overview using structured enrichment data.

---

## 2. Digital Maturity Analyzer

Combine website, business, and marketing intelligence into a normalized digital maturity score.

Levels:

* Basic
* Developing
* Intermediate
* Advanced
* Enterprise

---

## 3. Strength & Weakness Analyzer

Identify notable strengths and weaknesses using explainable rules.

Every insight should reference the supporting evidence from previous phases.

---

## 4. Opportunity Analyzer

Identify opportunities across:

* Website
* SEO
* Marketing
* Technology
* Sales
* Customer engagement

Rank opportunities by estimated business impact.

---

## 5. Service Recommendation Engine

Recommend relevant services based on identified gaps.

Examples:

* SEO
* PPC
* Website redesign
* Conversion optimization
* CRM implementation
* Marketing automation
* Analytics improvements
* Accessibility improvements

Each recommendation should include a short rationale.

---

## 6. Outreach Strategy Generator

Recommend:

* Best contact role
* Suggested outreach tone
* Recommended opening angle
* Supporting talking points

This module should leverage Decision Maker Discovery when available and gracefully fall back to role-based recommendations.

---

## 7. Risk Assessment

Highlight uncertainties, conflicting signals, and low-confidence estimates to keep recommendations transparent.

---

## Folder Structure

```text
src/
└── ai_insights/
    ├── models.py
    ├── executive_summary.py
    ├── digital_maturity.py
    ├── strengths.py
    ├── opportunities.py
    ├── recommendations.py
    ├── outreach.py
    ├── risks.py
    ├── engine.py
    └── validators.py
```

---

# Engineering Requirements

* Python 3.12+
* Async-first architecture
* Pydantic models
* SOLID principles
* Strong typing
* Structured logging
* Explainable outputs
* Confidence scoring
* No duplicate data collection
* Reuse outputs from Phases 01–06

---

# Deliverables

The completed phase must:

* Integrate into the enrichment pipeline.
* Extend `CompanyEnrichmentReport` with an `ai_insights` section.
* Update the CLI to display an **AI Insights (Phase 07)** summary.
* Include comprehensive unit, integration, and regression tests.
* Preserve compatibility with all previous phases.
* Produce deterministic, explainable recommendations suitable for downstream lead scoring.
