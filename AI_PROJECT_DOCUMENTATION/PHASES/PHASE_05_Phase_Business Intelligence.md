# Phase 05 — Business Intelligence

## Overview

Phase 05 enriches every discovered company with structured business intelligence.

The objective is to transform a simple website into a rich business profile that can be used for lead qualification, segmentation, AI insights, and lead scoring.

This phase consumes the outputs of:

* Phase 01 — Company Discovery
* Phase 02 — Website Intelligence
* Phase 03 — Contact Discovery
* Phase 04 — Decision Maker Discovery

No previous phases should be modified.

---

# Objectives

Automatically determine:

* Company type
* Industry
* Primary services
* Secondary services
* Service areas
* Company size
* Geographic footprint
* Years in business
* Business model
* Hiring signals
* Certifications
* Awards
* Customer testimonials
* Trust indicators

---

# Inputs

Each company already contains:

* Company Name
* Domain
* Website Intelligence
* Contact Information
* Decision Makers

---

# Expected Output

```json
{
  "business_intelligence": {
    "industry": "Roofing",
    "business_model": "B2B + B2C",
    "company_size": "Small Business",
    "estimated_employee_range": "11-50",
    "years_in_business": 18,
    "primary_services": [
      "Residential Roofing",
      "Commercial Roofing"
    ],
    "secondary_services": [
      "Roof Repair",
      "Gutter Installation"
    ],
    "service_areas": [
      "Dallas",
      "Fort Worth"
    ],
    "locations": 2,
    "certifications": [
      "GAF Certified"
    ],
    "awards": [
      "Best Roofing Contractor 2024"
    ],
    "trust_signals": {
      "testimonials": true,
      "case_studies": false,
      "portfolio": true,
      "financing": true,
      "warranty": true
    },
    "hiring": {
      "currently_hiring": false,
      "careers_page": true
    }
  }
}
```

---

# Modules

## 1. Industry Classifier

Determine the company's primary industry.

Examples:

* Roofing
* HVAC
* Plumbing
* Electrical
* Landscaping
* SaaS
* Marketing Agency
* Law Firm
* Dental Clinic
* Manufacturing

Use multiple signals:

* Website title
* Meta description
* Headings
* Navigation
* Structured data
* Service pages

---

## 2. Service Detection

Identify every service offered.

Examples:

Roofing

* Roof Repair
* Roof Replacement
* Commercial Roofing
* Metal Roofing
* Emergency Roofing

Marketing

* SEO
* PPC
* Web Design
* Branding
* Email Marketing

Return:

* Primary services
* Secondary services

---

## 3. Geographic Intelligence

Determine:

* Cities served
* States served
* Countries served
* Number of offices
* Headquarters

Sources:

* Contact pages
* Footer
* Structured data
* Location pages

---

## 4. Company Size Estimation

Estimate company size using public signals.

Signals include:

* Team page
* Number of staff mentioned
* Office count
* Careers page
* Scale of services
* Website content

Return an estimated employee range and confidence score.

---

## 5. Years in Business

Estimate business age using:

* "Founded in..."
* Copyright dates
* About page
* Company history

---

## 6. Business Model

Classify as:

* B2B
* B2C
* Both
* Non-profit
* Government

Use language across the website to infer the primary customer base.

---

## 7. Trust Signal Detection

Detect:

* Testimonials
* Reviews
* Case Studies
* Portfolio
* Certifications
* Awards
* Guarantees
* Warranties
* Financing options

---

## 8. Hiring Signals

Detect:

* Careers page
* Open positions
* Recruiting language
* Join our team
* Employment forms

---

# Folder Structure

```text
src/

business_intelligence/

    classifier.py
    service_detector.py
    geography.py
    company_size.py
    years_in_business.py
    business_model.py
    trust_signals.py
    hiring.py
    models.py
    validators.py
```

---

# Coding Standards

* Python 3.12+
* Async-first architecture
* Pydantic models
* Strong typing
* Modular design
* SOLID principles
* Structured logging
* Comprehensive unit tests
* Production-ready error handling

---

# Deliverables

The completed phase must:

* Integrate seamlessly with Phases 01–04.
* Produce structured Business Intelligence data.
* Generate a normalized JSON model.
* Include comprehensive unit and integration tests.
* Be production-ready for consumption by later phases (Marketing Intelligence, AI Insights, Lead Scoring, Export).
