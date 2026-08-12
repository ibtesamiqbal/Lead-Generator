"""
Unit tests for People Extractor parsing DOM team cards and JSON-LD.
"""

from src.decision_maker.models import Department
from src.decision_maker.people_extractor import PeopleExtractor
from src.enrichment.parser import HTMLParserDocument


def test_extract_people_from_json_ld():
    html = """
    <html>
    <head>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": "Jane Doe",
            "jobTitle": "CEO",
            "email": "jane@techcorp.com",
            "sameAs": "https://www.linkedin.com/in/janedoe"
        }
        </script>
    </head>
    <body></body>
    </html>
    """
    doc = HTMLParserDocument(html, base_url="https://techcorp.com")
    extractor = PeopleExtractor()

    people = extractor.extract_people(doc, source_url="https://techcorp.com")
    assert len(people) == 1
    p = people[0]
    assert p.full_name == "Jane Doe"
    assert p.normalized_title == "Chief Executive Officer"
    assert p.department == Department.EXECUTIVE
    assert p.email == "jane@techcorp.com"
    assert p.linkedin_url == "https://www.linkedin.com/in/janedoe"


def test_extract_people_from_html_cards():
    html = """
    <html>
    <body>
        <div class="team-member">
            <h3>Robert Johnson</h3>
            <p class="title">VP Sales</p>
            <p class="bio">Robert leads global sales strategy with over 15 years of industry experience.</p>
            <a href="https://www.linkedin.com/in/robert-johnson">LinkedIn Profile</a>
            <a href="mailto:robert@techcorp.com">Email Robert</a>
        </div>
        <div class="team-member">
            <h3>Alice Williams</h3>
            <p class="title">CTO</p>
            <p class="bio">Alice manages cloud engineering and technology architecture.</p>
            <a href="https://www.linkedin.com/in/alice-williams">LinkedIn Profile</a>
        </div>
    </body>
    </html>
    """
    doc = HTMLParserDocument(html, base_url="https://techcorp.com/team")
    extractor = PeopleExtractor()

    people = extractor.extract_people(doc, source_url="https://techcorp.com/team")
    assert len(people) == 2

    names = {p.full_name for p in people}
    assert "Robert Johnson" in names
    assert "Alice Williams" in names

    robert = next(p for p in people if p.full_name == "Robert Johnson")
    assert robert.normalized_title == "Vice President Sales"
    assert robert.department == Department.SALES
    assert robert.email == "robert@techcorp.com"
    assert robert.priority == 70
