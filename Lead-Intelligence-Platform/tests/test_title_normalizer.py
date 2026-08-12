"""
Unit tests for Title Normalizer, Department Classifier, and Seniority Classifier.
"""

from src.decision_maker.models import Department, Seniority
from src.decision_maker.title_normalizer import TitleNormalizer


def test_title_normalization_examples():
    assert TitleNormalizer.normalize_title("CEO") == "Chief Executive Officer"
    assert TitleNormalizer.normalize_title("VP Sales") == "Vice President Sales"
    assert TitleNormalizer.normalize_title("Head of Sales") == "Head of Sales"
    assert TitleNormalizer.normalize_title("Owner") == "Owner"
    assert TitleNormalizer.normalize_title("Founder") == "Founder"
    assert TitleNormalizer.normalize_title("CTO") == "Chief Technology Officer"
    assert TitleNormalizer.normalize_title("COO") == "Chief Operating Officer"
    assert TitleNormalizer.normalize_title("CFO") == "Chief Financial Officer"
    assert TitleNormalizer.normalize_title("CMO") == "Chief Marketing Officer"
    assert TitleNormalizer.normalize_title("Co-Founder & CEO") == "Co-Founder & Chief Executive Officer"


def test_department_classification():
    assert TitleNormalizer.classify_department("Chief Executive Officer") == Department.EXECUTIVE
    assert TitleNormalizer.classify_department("Founder") == Department.EXECUTIVE
    assert TitleNormalizer.classify_department("Chief Technology Officer") == Department.TECHNOLOGY
    assert TitleNormalizer.classify_department("VP Sales") == Department.SALES
    assert TitleNormalizer.classify_department("Head of Marketing") == Department.MARKETING
    assert TitleNormalizer.classify_department("General Manager") == Department.OPERATIONS
    assert TitleNormalizer.classify_department("Chief Financial Officer") == Department.FINANCE
    assert TitleNormalizer.classify_department("Head of People") == Department.HUMAN_RESOURCES


def test_seniority_classification():
    assert TitleNormalizer.classify_seniority("Chief Executive Officer") == Seniority.EXECUTIVE
    assert TitleNormalizer.classify_seniority("Founder") == Seniority.EXECUTIVE
    assert TitleNormalizer.classify_seniority("Vice President Sales") == Seniority.VP
    assert TitleNormalizer.classify_seniority("Sales Director") == Seniority.DIRECTOR
    assert TitleNormalizer.classify_seniority("Head of Product") == Seniority.HEAD
    assert TitleNormalizer.classify_seniority("General Manager") == Seniority.MANAGER
