"""
Async HTTP Fetcher Module for Website Intelligence Extraction.
Uses httpx.AsyncClient with session reuse, retries, exponential backoff, and graceful error handling.
"""

import asyncio
import time
import httpx
from src.config.settings import settings
from src.enrichment.models import FetchResult
from src.logging.logger import logger


class HTTPFetcher:
    """Resilient Async HTTP Fetcher."""

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        user_agent: str | None = None,
    ):
        self._external_client = client
        self.timeout = timeout or settings.scraping.timeout_seconds
        self.max_retries = max_retries or settings.scraping.max_retries
        self.user_agent = user_agent or settings.scraping.user_agent

    async def fetch(self, url: str) -> FetchResult:
        """
        Fetches webpage content asynchronously with retry strategy and exponential backoff.
        
        Args:
            url: Target URL to fetch
            
        Returns:
            FetchResult object containing response metadata or error info.
        """
        target_url = url if url.startswith(("http://", "https://")) else f"https://{url}"
        # Dynamically check brotli availability to prevent unreadable Brotli binary payloads
        accept_encoding = "gzip, deflate"
        try:
            import importlib.util
            if importlib.util.find_spec("brotli") or importlib.util.find_spec("brotlicffi"):
                accept_encoding = "gzip, deflate, br"
        except Exception:
            pass

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": accept_encoding,
        }

        should_close = False
        client = self._external_client

        if client is None:
            client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=True,
                headers=headers,
            )
            should_close = True

        start_time = time.perf_counter()
        attempt = 0
        last_error = ""

        try:
            while attempt <= self.max_retries:
                attempt += 1
                try:
                    response = await client.get(target_url, headers=headers)
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

                    resp_headers = {k.lower(): v for k, v in response.headers.items()}
                    is_success = 200 <= response.status_code < 300

                    # Safe HTML content extraction
                    try:
                        content_text = response.text
                    except Exception:
                        content_text = response.content.decode("utf-8", errors="replace")

                    return FetchResult(
                        url=str(response.url),
                        status_code=response.status_code,
                        content=content_text,
                        headers=resp_headers,
                        response_time_ms=round(elapsed_ms, 2),
                        is_success=is_success,
                        error=None if is_success else f"HTTP Status {response.status_code}"
                    )

                except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                    last_error = f"{type(exc).__name__}: {exc}"
                    logger.warning(
                        f"Fetch attempt {attempt}/{self.max_retries + 1} failed for '{target_url}': {last_error}"
                    )
                    if attempt <= self.max_retries:
                        backoff = (settings.scraping.backoff_factor ** attempt) * 0.5
                        try:
                            import anyio
                            await anyio.sleep(backoff)
                        except Exception:
                            await asyncio.sleep(backoff)

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return FetchResult(
                url=target_url,
                status_code=0,
                content="",
                headers={},
                response_time_ms=round(elapsed_ms, 2),
                is_success=False,
                error=f"Exhausted {self.max_retries + 1} attempts. Last error: {last_error}"
            )

        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"Unexpected error fetching '{target_url}': {err}")
            return FetchResult(
                url=target_url,
                status_code=0,
                content="",
                headers={},
                response_time_ms=round(elapsed_ms, 2),
                is_success=False,
                error=str(err)
            )

        finally:
            if should_close and client is not None:
                await client.aclose()
