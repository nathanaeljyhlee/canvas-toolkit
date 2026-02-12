"""Tests for Canvas client input validation."""

import pytest
from canvas_toolkit.client import CanvasClient


class TestCanvasClientValidation:
    """Test suite for CanvasClient input validation."""

    def test_valid_url_and_token(self):
        """Test that valid inputs are accepted."""
        client = CanvasClient(
            base_url="https://babson.instructure.com",
            api_token="valid_token_123"
        )
        assert client.base_url == "https://babson.instructure.com"
        assert client.api_token == "valid_token_123"

    def test_url_trailing_slash_removed(self):
        """Test that trailing slash is removed from URL."""
        client = CanvasClient(
            base_url="https://babson.instructure.com/",
            api_token="token"
        )
        assert client.base_url == "https://babson.instructure.com"

    def test_empty_url_rejected(self):
        """Test that empty URL is rejected."""
        with pytest.raises(ValueError, match="base_url must be a non-empty string"):
            CanvasClient(base_url="", api_token="token")

    def test_none_url_rejected(self):
        """Test that None URL is rejected."""
        with pytest.raises(ValueError, match="base_url must be a non-empty string"):
            CanvasClient(base_url=None, api_token="token")

    def test_empty_token_rejected(self):
        """Test that empty token is rejected."""
        with pytest.raises(ValueError, match="api_token must be a non-empty string"):
            CanvasClient(base_url="https://example.com", api_token="")

    def test_none_token_rejected(self):
        """Test that None token is rejected."""
        with pytest.raises(ValueError, match="api_token must be a non-empty string"):
            CanvasClient(base_url="https://example.com", api_token=None)

    def test_invalid_url_format_rejected(self):
        """Test that malformed URLs are rejected."""
        with pytest.raises(ValueError, match="Invalid Canvas URL"):
            CanvasClient(base_url="not-a-url", api_token="token")

    def test_url_without_scheme_rejected(self):
        """Test that URL without http/https is rejected."""
        with pytest.raises(ValueError, match="Invalid Canvas URL"):
            CanvasClient(base_url="babson.instructure.com", api_token="token")

    def test_invalid_scheme_rejected(self):
        """Test that non-http/https schemes are rejected."""
        with pytest.raises(ValueError, match="Canvas URL must use http or https"):
            CanvasClient(base_url="ftp://example.com", api_token="token")

    def test_http_url_accepted(self):
        """Test that http (not https) is accepted for local dev."""
        client = CanvasClient(
            base_url="http://localhost:3000",
            api_token="token"
        )
        assert client.base_url == "http://localhost:3000"

    def test_non_string_url_rejected(self):
        """Test that non-string URLs are rejected."""
        with pytest.raises(ValueError, match="base_url must be a non-empty string"):
            CanvasClient(base_url=123, api_token="token")

    def test_non_string_token_rejected(self):
        """Test that non-string tokens are rejected."""
        with pytest.raises(ValueError, match="api_token must be a non-empty string"):
            CanvasClient(base_url="https://example.com", api_token=123)
