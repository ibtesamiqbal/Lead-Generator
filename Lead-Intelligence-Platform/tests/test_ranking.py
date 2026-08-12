"""
Unit tests for Decision Maker Priority Ranking and Confidence Scoring.
"""

from src.decision_maker.models import DecisionMaker, Department, Seniority
from src.decision_maker.ranking import DecisionMakerRanker


def test_priority_ranking_tiers():
    # Priority 100
    assert DecisionMakerRanker.calculate_priority("Chief Executive Officer", Department.EXECUTIVE, Seniority.EXECUTIVE) == 100
    assert DecisionMakerRanker.calculate_priority("Founder", Department.EXECUTIVE, Seniority.EXECUTIVE) == 100
    assert DecisionMakerRanker.calculate_priority("Owner", Department.EXECUTIVE, Seniority.EXECUTIVE) == 100
    assert DecisionMakerRanker.calculate_priority("President", Department.EXECUTIVE, Seniority.EXECUTIVE) == 100

    # Priority 90
    assert DecisionMakerRanker.calculate_priority("Managing Director", Department.EXECUTIVE, Seniority.EXECUTIVE) == 90
    assert DecisionMakerRanker.calculate_priority("Co-Founder", Department.EXECUTIVE, Seniority.EXECUTIVE) == 90
    assert DecisionMakerRanker.calculate_priority("Partner", Department.EXECUTIVE, Seniority.EXECUTIVE) == 90

    # Priority 80
    assert DecisionMakerRanker.calculate_priority("Chief Technology Officer", Department.TECHNOLOGY, Seniority.EXECUTIVE) == 80
    assert DecisionMakerRanker.calculate_priority("Chief Operating Officer", Department.OPERATIONS, Seniority.EXECUTIVE) == 80
    assert DecisionMakerRanker.calculate_priority("Chief Financial Officer", Department.FINANCE, Seniority.EXECUTIVE) == 80
    assert DecisionMakerRanker.calculate_priority("Chief Marketing Officer", Department.MARKETING, Seniority.EXECUTIVE) == 80

    # Priority 70
    assert DecisionMakerRanker.calculate_priority("Vice President Sales", Department.SALES, Seniority.VP) == 70
    assert DecisionMakerRanker.calculate_priority("Sales Director", Department.SALES, Seniority.DIRECTOR) == 70
    assert DecisionMakerRanker.calculate_priority("Head of Sales", Department.SALES, Seniority.HEAD) == 70
    assert DecisionMakerRanker.calculate_priority("Business Development Director", Department.SALES, Seniority.DIRECTOR) == 70


def test_confidence_scoring():
    score = DecisionMakerRanker.calculate_confidence(
        is_leadership_page=True,
        has_recognized_title=True,
        has_biography=True,
        multiple_mentions=True,
        has_contact_info=True,
        has_clean_name=True
    )
    assert score == 1.0

    score_minimal = DecisionMakerRanker.calculate_confidence(
        is_leadership_page=False,
        has_recognized_title=False,
        has_biography=False
    )
    assert score_minimal == 0.15


def test_rank_decision_makers_sorting():
    dm1 = DecisionMaker(full_name="VP Sales Person", title="VP Sales", normalized_title="Vice President Sales", priority=70, confidence=0.8, source_url="http://ex.com")
    dm2 = DecisionMaker(full_name="CEO Person", title="CEO", normalized_title="Chief Executive Officer", priority=100, confidence=0.9, source_url="http://ex.com")
    dm3 = DecisionMaker(full_name="CTO Person", title="CTO", normalized_title="Chief Technology Officer", priority=80, confidence=0.85, source_url="http://ex.com")

    sorted_dms = DecisionMakerRanker.rank_decision_makers([dm1, dm2, dm3])
    assert sorted_dms[0].full_name == "CEO Person"
    assert sorted_dms[1].full_name == "CTO Person"
    assert sorted_dms[2].full_name == "VP Sales Person"
