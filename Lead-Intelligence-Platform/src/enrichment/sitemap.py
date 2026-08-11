"""
Sitemap XML Parser Module.
Fetches, validates, and parses XML sitemaps and sitemap index entries.
"""

import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.models import SitemapData
from src.logging.logger import logger


class SitemapParser:
    """Parses XML sitemaps and collects indexed page URLs."""

    def __init__(self, fetcher: HTTPFetcher | None = None):
        self.fetcher = fetcher or HTTPFetcher()

    async def fetch_and_parse(self, domain_or_url: str, sitemap_url_override: str | None = None) -> SitemapData:
        """
        Fetches and parses sitemap.xml for a target domain.
        """
        base_url = domain_or_url if domain_or_url.startswith(("http://", "https://")) else f"https://{domain_or_url}"
        target_sitemap = sitemap_url_override or urljoin(base_url, "/sitemap.xml")

        result = await self.fetcher.fetch(target_sitemap)
        if not result.is_success or not result.content.strip():
            return SitemapData(is_found=False, sitemap_urls=[], url_count=0)

        urls = set()
        try:
            # Strip XML namespace tags if present for simplified parsing
            clean_xml = result.content
            root = ET.fromstring(clean_xml)

            # Namespace map handling
            namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # Find <loc> elements
            for elem in root.findall('.//{*}loc'):
                if elem.text:
                    loc_str = elem.text.strip()
                    if loc_str.startswith(("http://", "https://")):
                        urls.add(loc_str)

            return SitemapData(
                is_found=True,
                sitemap_urls=sorted(list(urls)),
                url_count=len(urls)
            )

        except ET.ParseError as err:
            logger.warning(f"Failed to parse sitemap XML for '{target_sitemap}': {err}")
            return SitemapData(is_found=False, sitemap_urls=[], url_count=0)
