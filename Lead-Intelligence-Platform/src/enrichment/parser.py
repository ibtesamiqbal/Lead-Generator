"""
Safe HTML Parsing Module for Website Intelligence Extraction.
Wraps BeautifulSoup with lxml/html.parser fallback and helper extraction methods.
"""

from bs4 import BeautifulSoup, Tag
from src.logging.logger import logger


class HTMLParserDocument:
    """Encapsulates a parsed HTML DOM document with safe helper queries."""

    def __init__(self, raw_html: str, base_url: str = ""):
        self.raw_html = raw_html or ""
        self.base_url = base_url
        self.soup = self._parse_html(self.raw_html)

    def _parse_html(self, html: str) -> BeautifulSoup:
        """Safely parses HTML string with parser engine fallback."""
        if not html.strip():
            return BeautifulSoup("", "html.parser")
        try:
            return BeautifulSoup(html, "lxml")
        except Exception:
            try:
                return BeautifulSoup(html, "html.parser")
            except Exception as err:
                logger.warning(f"Failed to parse HTML document: {err}")
                return BeautifulSoup("", "html.parser")

    def get_title(self) -> str | None:
        """Extracts text content of <title> tag."""
        if self.soup.title:
            title_text = self.soup.title.get_text(strip=True)
            return title_text if title_text else None
        return None

    def get_meta_content(self, name_or_property: str) -> str | None:
        """Extracts content attribute of a meta tag by name or property attribute."""
        meta = self.soup.find(
            "meta",
            attrs={"name": name_or_property}
        ) or self.soup.find(
            "meta",
            attrs={"property": name_or_property}
        )
        if isinstance(meta, Tag) and meta.get("content"):
            content = str(meta.get("content")).strip()
            return content if content else None
        return None

    def get_all_meta_tags(self) -> list[dict[str, str]]:
        """Extracts list of all meta tag attributes."""
        meta_list = []
        for tag in self.soup.find_all("meta"):
            if isinstance(tag, Tag):
                attrs = {k: str(v) for k, v in tag.attrs.items() if isinstance(v, (str, list))}
                meta_list.append(attrs)
        return meta_list

    def get_headings(self, level: str = "h1") -> list[str]:
        """Extracts text content of heading tags (e.g. h1, h2)."""
        tag_name = level.lower().strip()
        headings = []
        for tag in self.soup.find_all(tag_name):
            text = tag.get_text(strip=True)
            if text:
                headings.append(text)
        return headings

    def get_all_links(self) -> list[dict[str, str]]:
        """Extracts list of all anchor <a> links with href and text."""
        links = []
        for a in self.soup.find_all("a", href=True):
            if isinstance(a, Tag):
                href = str(a.get("href", "")).strip()
                text = a.get_text(strip=True)
                if href:
                    links.append({"href": href, "text": text})
        return links

    def get_text_content(self) -> str:
        """Extracts visible text content from document body."""
        if self.soup.body:
            return self.soup.body.get_text(separator=" ", strip=True)
        return self.soup.get_text(separator=" ", strip=True)

    def get_html_attribute(self, attr: str = "lang") -> str | None:
        """Extracts attribute from top-level <html> tag."""
        html_tag = self.soup.find("html")
        if isinstance(html_tag, Tag) and html_tag.get(attr):
            val = str(html_tag.get(attr)).strip()
            return val if val else None
        return None
