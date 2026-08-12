"""
Multi-Industry Integration Test Suite for Decision Maker Discovery (Phase 04).
Validates discovery, extraction, title normalization, department classification,
and ranking across 10 diverse B2B industry company archetypes:
1. Roofing
2. Movers
3. HVAC
4. Plumbing
5. Landscaping
6. Law Firms
7. Dental Clinics
8. SaaS
9. Manufacturing
10. Marketing Agencies
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.decision_maker.discovery import DecisionMakerDiscoveryEngine
from src.decision_maker.models import Department, Seniority
from src.enrichment.fetcher import FetchResult
from src.enrichment.parser import HTMLParserDocument


INDUSTRY_SAMPLE_PAGES = {
    "roofing": {
        "domain": "apexroofingpro.com.au",
        "home": "<html><body><nav><a href='/our-team'>Meet Our Roofing Team</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Dave Miller</h2>
                <p class="title">Owner & General Manager</p>
                <p class="bio">Dave has run Apex Roofing for over 20 years.</p>
                <a href="mailto:dave@apexroofingpro.com.au">Contact Dave</a>
            </div>
            <div class="team-member">
                <h2>Chris Vance</h2>
                <p class="title">Head of Sales</p>
            </div>
        </body></html>"""
    },
    "movers": {
        "domain": "swiftrelocations.com",
        "home": "<html><body><nav><a href='/about'>About Our Moving Company</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Marcus Sterling</h2>
                <p class="title">Managing Director</p>
            </div>
            <div class="team-member">
                <h2>Sarah Jenkins</h2>
                <p class="title">Operations Director</p>
            </div>
        </body></html>"""
    },
    "hvac": {
        "domain": "coolairhvac.com",
        "home": "<html><body><nav><a href='/leadership'>Leadership</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Tom Bradley</h2>
                <p class="title">President & Founder</p>
            </div>
        </body></html>"""
    },
    "plumbing": {
        "domain": "propipeplumbing.com",
        "home": "<html><body><nav><a href='/team'>Our Plumbing Team</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>James Wright</h2>
                <p class="title">Owner</p>
            </div>
        </body></html>"""
    },
    "landscaping": {
        "domain": "greenvalleylandscaping.com",
        "home": "<html><body><nav><a href='/about-us'>About Us</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Elena Torres</h2>
                <p class="title">Co-Founder & CEO</p>
            </div>
        </body></html>"""
    },
    "law_firm": {
        "domain": "justicepartnerslaw.com",
        "home": "<html><body><nav><a href='/people'>Attorneys & Leadership</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Richard Harrison</h2>
                <p class="title">Managing Partner</p>
            </div>
            <div class="team-member">
                <h2>Victoria Chen</h2>
                <p class="title">Partner</p>
            </div>
        </body></html>"""
    },
    "dental": {
        "domain": "smiledentalcare.com",
        "home": "<html><body><nav><a href='/staff'>Our Dental Team</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Dr. Amanda Ross</h2>
                <p class="title">Owner & Lead Dentist</p>
            </div>
        </body></html>"""
    },
    "saas": {
        "domain": "cloudstackio.com",
        "home": "<html><body><nav><a href='/company'>Company Executives</a></nav></body></html>",
        "team": """<html><body>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "employee": [
                    {"@type": "Person", "name": "Alex Mercer", "jobTitle": "CEO & Co-Founder"},
                    {"@type": "Person", "name": "Dr. Priya Patel", "jobTitle": "CTO"},
                    {"@type": "Person", "name": "Jason Reed", "jobTitle": "VP Sales"}
                ]
            }
            </script>
        </body></html>"""
    },
    "manufacturing": {
        "domain": "precisionindustries.com",
        "home": "<html><body><nav><a href='/leadership'>Executive Management</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Heinrich Weber</h2>
                <p class="title">Chief Executive Officer</p>
            </div>
            <div class="team-member">
                <h2>Kurt Meyer</h2>
                <p class="title">Chief Operating Officer</p>
            </div>
        </body></html>"""
    },
    "marketing_agency": {
        "domain": "nexusdigitalagency.com",
        "home": "<html><body><nav><a href='/team'>Meet the Crew</a></nav></body></html>",
        "team": """<html><body>
            <div class="team-member">
                <h2>Chloe Bennett</h2>
                <p class="title">Founder & CEO</p>
            </div>
            <div class="team-member">
                <h2>Liam O'Connor</h2>
                <p class="title">Marketing Director</p>
            </div>
        </body></html>"""
    }
}


@pytest.mark.anyio
@pytest.mark.parametrize("industry_key", list(INDUSTRY_SAMPLE_PAGES.keys()))
async def test_multi_industry_decision_maker_discovery(industry_key: str):
    data = INDUSTRY_SAMPLE_PAGES[industry_key]
    domain = data["domain"]
    home_html = data["home"]
    team_html = data["team"]

    mock_fetcher = MagicMock()
    mock_fetcher.fetch = AsyncMock(return_value=FetchResult(
        url=f"https://{domain}/team",
        status_code=200,
        content=team_html,
        is_success=True
    ))

    engine = DecisionMakerDiscoveryEngine(fetcher=mock_fetcher)
    doc = HTMLParserDocument(home_html, base_url=f"https://{domain}")

    report = await engine.discover(domain, doc, source_url=f"https://{domain}")

    assert report.domain == domain
    assert report.is_successful is True
    assert report.total_people_found >= 1

    top_dm = report.decision_makers[0]
    assert top_dm.priority >= 70
    assert top_dm.normalized_title != "Unknown"
    assert top_dm.department in (Department.EXECUTIVE, Department.TECHNOLOGY, Department.SALES, Department.OPERATIONS)
