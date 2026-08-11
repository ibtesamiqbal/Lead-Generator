"""
Business Operating Hours Finder Module.
Extracts published operating hours from HTML DOM text and Schema.org markup.
"""

import re
from src.contact_discovery.models import BusinessHours
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class BusinessHoursFinder:
    """Discovers and parses business operating hours from webpage text."""

    HOURS_REGEX = re.compile(
        r'(?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)'
        r'(?:\s*-\s*(?:Mon(?:day)?|Tue(?:sday)?|Wed(?:nesday)?|Thu(?:rsday)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?))?'
        r':?\s*(?:\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?\s*-\s*\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?|Closed)',
        re.IGNORECASE
    )

    def find_hours(self, doc: HTMLParserDocument, source_url: str = "") -> BusinessHours | None:
        """
        Parses operating hours patterns into structured days/hours dictionary.
        """
        raw_text = doc.soup.get_text()
        matches = self.HOURS_REGEX.findall(raw_text)

        if not matches:
            return None

        schedule = {}
        for m in matches:
            parts = m.split(":", 1)
            if len(parts) == 2:
                day_part = parts[0].strip()
                time_part = parts[1].strip()
                schedule[day_part] = time_part
            else:
                schedule["General"] = m.strip()

        return BusinessHours(
            schedule=schedule,
            raw_text="; ".join(matches),
            source_url=source_url
        )
