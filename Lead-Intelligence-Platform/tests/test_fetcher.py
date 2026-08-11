"""
Unit Tests for HTTPFetcher.
Mocks all HTTP requests using httpx.MockTransport.
"""

import pytest
import httpx
from src.enrichment.fetcher import HTTPFetcher


@pytest.mark.anyio
async def test_fetcher_success():
    """Test successful 200 OK fetch with MockTransport."""
    def handler(request):
        return httpx.Response(200, text="<html><head><title>Test Page</title></head></html>")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        result = await fetcher.fetch("https://example.com")

        assert result.is_success is True
        assert result.status_code == 200
        assert "Test Page" in result.content
        assert result.error is None


@pytest.mark.anyio
async def test_fetcher_http_404_failure():
    """Test handling of 404 Not Found response."""
    def handler(request):
        return httpx.Response(404, text="Not Found")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client)
        result = await fetcher.fetch("https://example.com/missing")

        assert result.is_success is False
        assert result.status_code == 404
        assert result.error == "HTTP Status 404"


@pytest.mark.anyio
async def test_fetcher_timeout_resilience():
    """Test handling of network timeout exception."""
    def handler(request):
        raise httpx.TimeoutException("Connection timed out", request=request)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        fetcher = HTTPFetcher(client=client, max_retries=1)
        result = await fetcher.fetch("https://example.com/timeout")

        assert result.is_success is False
        assert result.status_code == 0
        assert "Exhausted 2 attempts" in result.error
