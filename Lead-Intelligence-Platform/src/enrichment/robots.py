"""
Robots.txt Parser Module.
Fetches and parses user-agent disallow/allow rules and referenced XML sitemap entries.
"""

from urllib.parse import urljoin
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.models import RobotsTxtData
from src.logging.logger import logger


class RobotsTxtParser:
    """Parses robots.txt rules and sitemap entries."""

    def __init__(self, fetcher: HTTPFetcher | None = None):
        self.fetcher = fetcher or HTTPFetcher()

    async def fetch_and_parse(self, domain_or_url: str) -> RobotsTxtData:
        """
        Fetches /robots.txt for domain and parses directives.
        """
        base_url = domain_or_url if domain_or_url.startswith(("http://", "https://")) else f"https://{domain_or_url}"
        robots_url = urljoin(base_url, "/robots.txt")

        result = await self.fetcher.fetch(robots_url)
        if not result.is_success or not result.content.strip():
            return RobotsTxtData(is_found=False, rules=[], sitemap_urls=[], raw_text=None)

        rules = []
        sitemap_urls = []
        current_ua = "*"

        for line in result.content.splitlines():
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue

            if ":" in line_str:
                parts = line_str.split(":", 1)
                directive = parts[0].strip().lower()
                value = parts[1].strip()

                if directive == "user-agent":
                    current_ua = value
                elif directive in ("disallow", "allow"):
                    rules.append({
                        "user_agent": current_ua,
                        "directive": directive,
                        "path": value
                    })
                elif directive == "sitemap":
                    if value.startswith(("http://", "https://")):
                        sitemap_urls.append(value)

        return RobotsTxtData(
            is_found=True,
            rules=rules,
            sitemap_urls=sorted(list(set(sitemap_urls))),
            raw_text=result.content[:5000]  # Store up to 5 KB snippet
        )
