"""
Metadata Extractor Module.
Extracts title, meta descriptions, canonical URLs, OG tags, Twitter cards, headings, and charset metadata.
"""

from urllib.parse import urljoin
from bs4 import Tag
from src.enrichment.models import WebsiteMetadata
from src.enrichment.parser import HTMLParserDocument


class MetadataExtractor:
    """Extracts structured metadata from HTML document."""

    def extract(self, doc: HTMLParserDocument, base_url: str = "") -> WebsiteMetadata:
        """
        Extracts all HTML document metadata attributes into a WebsiteMetadata model.
        """
        title = doc.get_title()
        meta_desc = doc.get_meta_content("description")
        meta_keywords_raw = doc.get_meta_content("keywords")
        keywords = [k.strip() for k in meta_keywords_raw.split(",")] if meta_keywords_raw else []

        canonical = self._extract_canonical(doc, base_url)
        og_tags = self._extract_prefix_meta(doc, prefix="og:")
        twitter_tags = self._extract_prefix_meta(doc, prefix="twitter:")

        h1_tags = doc.get_headings("h1")
        h2_tags = doc.get_headings("h2")

        language = doc.get_html_attribute("lang")
        charset = self._extract_charset(doc)
        favicon = self._extract_favicon(doc, base_url)
        generator = doc.get_meta_content("generator")

        # Fallback to OG title, Twitter title, or H1 tag if primary <title> tag is missing
        if not title:
            title = og_tags.get("og:title") or twitter_tags.get("twitter:title") or (h1_tags[0] if h1_tags else None)

        return WebsiteMetadata(
            title=title,
            meta_description=meta_desc,
            canonical_url=canonical,
            keywords=keywords,
            open_graph=og_tags,
            twitter_card=twitter_tags,
            h1_tags=h1_tags,
            h2_tags=h2_tags,
            language=language,
            charset=charset,
            favicon_url=favicon,
            generator=generator
        )

    def _extract_canonical(self, doc: HTMLParserDocument, base_url: str) -> str | None:
        link = doc.soup.find("link", attrs={"rel": "canonical"})
        if isinstance(link, Tag) and link.get("href"):
            href = str(link.get("href")).strip()
            return urljoin(base_url, href) if base_url else href
        return None

    def _extract_prefix_meta(self, doc: HTMLParserDocument, prefix: str) -> dict[str, str]:
        results = {}
        for tag in doc.soup.find_all("meta"):
            if isinstance(tag, Tag):
                prop = str(tag.get("property", "") or tag.get("name", "")).strip()
                content = str(tag.get("content", "")).strip()
                if prop.startswith(prefix) and content:
                    results[prop] = content
        return results

    def _extract_charset(self, doc: HTMLParserDocument) -> str | None:
        meta_charset = doc.soup.find("meta", attrs={"charset": True})
        if isinstance(meta_charset, Tag) and meta_charset.get("charset"):
            return str(meta_charset.get("charset")).strip()

        content_type = doc.get_meta_content("content-type")
        if content_type and "charset=" in content_type.lower():
            return content_type.lower().split("charset=")[-1].strip()
        return None

    def _extract_favicon(self, doc: HTMLParserDocument, base_url: str) -> str | None:
        icon_link = (
            doc.soup.find("link", attrs={"rel": "shortcut icon"}) or
            doc.soup.find("link", attrs={"rel": "icon"}) or
            doc.soup.find("link", attrs={"rel": lambda r: r and "icon" in r.lower() if isinstance(r, str) else False})
        )
        if isinstance(icon_link, Tag) and icon_link.get("href"):
            href = str(icon_link.get("href")).strip()
            return urljoin(base_url, href) if base_url else href
        return None
