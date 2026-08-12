# Phase 04 — Decision Maker Discovery

## Overview

Phase 04 is responsible for identifying the most relevant people within a company who are responsible for purchasing decisions or executive leadership.

This phase consumes the output of previous phases and enriches each discovered company with structured decision-maker information.

---

# Previous Phases

✅ Phase 01 — Company Discovery

* Company Discovery
* Company Validation
* Website Discovery

✅ Phase 02 — Website Intelligence

* Website Crawling
* Technology Detection
* SEO Analysis
* Website Metadata

✅ Phase 03 — Contact Discovery

* Emails
* Phone Numbers
* Addresses
* Contact Pages
* Business Hours
* Social Profiles

---

# Objective

Automatically discover decision makers from company websites and publicly accessible information.

The goal is to identify the best people for sales outreach.

---

# Inputs

Each company already contains:

* Company Name
* Website
* Industry
* Website Intelligence
* Contact Information

---

# Outputs

Each company should be enriched with:

* Full Name
* Job Title
* Department
* Seniority
* Priority Score
* Confidence Score
* Source URL
* LinkedIn URL (if present on company website)
* Public Email (if available)
* Public Phone (if available)

---

# Decision Makers to Detect

Highest Priority

* Founder
* Co-Founder
* CEO
* Owner
* President
* Managing Director

Executive

* CTO
* COO
* CIO
* CFO
* CMO

Sales

* VP Sales
* Head of Sales
* Sales Director
* Business Development Director

Operations

* Operations Director
* General Manager

Marketing

* Marketing Director
* Growth Director

---

# Discovery Strategy

## Step 1

Locate leadership pages.

Examples:

* /about
* /about-us
* /team
* /our-team
* /leadership
* /management
* /company
* /staff
* /people
* /executives

Also inspect:

* Navigation menus
* Footer links
* Sitemap
* Internal links

---

## Step 2

Extract every discovered person.

Fields:

* Name
* Title
* Biography
* Image
* Email
* Phone
* LinkedIn URL
* Source URL

---

## Step 3

Normalize titles.

Example:

CEO

↓

Chief Executive Officer

VP Sales

↓

Vice President Sales

Owner

↓

Owner

---

## Step 4

Department Classification

Executive

Sales

Marketing

Operations

Technology

Finance

Human Resources

---

## Step 5

Priority Ranking

Priority 100

Founder

CEO

Owner

President

Priority 90

Managing Director

Partner

Co-Founder

Priority 80

CTO

COO

CMO

CFO

Priority 70

VP Sales

Sales Director

Head of Sales

Business Development Director

---

## Step 6

Confidence Score

Leadership page found

*

Executive title recognized

*

Person appears multiple times

*

Profile contains biography

*

Company branding matches

=

Confidence Score

---

# JSON Model

Each discovered person should contain:

* id
* full_name
* first_name
* last_name
* title
* normalized_title
* department
* seniority
* email
* phone
* linkedin_url
* biography
* image
* source_url
* confidence
* priority

---

# Folder Structure

src/

decision_maker/

* discovery.py
* website_scanner.py
* people_extractor.py
* title_normalizer.py
* ranking.py
* models.py
* validators.py

tests/

* test_discovery.py
* test_people_extractor.py
* test_ranking.py

---

# Coding Standards

* Python 3.12+
* Async-first
* Strong typing
* Pydantic models
* Modular architecture
* Comprehensive logging
* Retry support
* Production-ready error handling
* Unit tests
* Fully documented

---

# Deliverables

At the end of this phase, every company should include a ranked list of decision makers with normalized titles, confidence scores, and structured output that can be consumed by later enrichment and scoring phases.
