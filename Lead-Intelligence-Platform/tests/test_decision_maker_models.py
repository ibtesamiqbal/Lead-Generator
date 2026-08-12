"""
Unit tests for Decision Maker Discovery models (Phase 04).
"""

from src.decision_maker.models import (
    DecisionMaker,
    DecisionMakerDiscoveryReport,
    Department,
    LeadershipPage,
    Seniority,
)


def test_decision_maker_model_instantiation():
    dm = DecisionMaker(
        full_name="Sarah Connor",
        first_name="Sarah",
        last_name="Connor",
        title="CEO",
        normalized_title="Chief Executive Officer",
        department=Department.EXECUTIVE,
        seniority=Seniority.EXECUTIVE,
        email="sarah@skynet.com",
        linkedin_url="https://linkedin.com/in/sarah-connor",
        source_url="https://example.com/team",
        confidence=0.95,
        priority=100
    )

    assert dm.full_name == "Sarah Connor"
    assert dm.normalized_title == "Chief Executive Officer"
    assert dm.department == Department.EXECUTIVE
    assert dm.seniority == Seniority.EXECUTIVE
    assert dm.priority == 100
    assert dm.confidence == 0.95
    assert dm.id is not None


def test_leadership_page_model():
    page = LeadershipPage(
        url="https://example.com/leadership",
        title="Our Executive Team",
        confidence=0.85,
        source="Navigation Menu"
    )

    assert page.url == "https://example.com/leadership"
    assert page.confidence == 0.85


def test_decision_maker_discovery_report():
    report = DecisionMakerDiscoveryReport(
        domain="example.com",
        total_people_found=1,
        decision_makers=[
            DecisionMaker(
                full_name="John Doe",
                title="CTO",
                normalized_title="Chief Technology Officer",
                source_url="https://example.com/team"
            )
        ]
    )

    assert report.domain == "example.com"
    assert report.total_people_found == 1
    assert report.decision_makers[0].normalized_title == "Chief Technology Officer"
    assert report.is_successful is True
