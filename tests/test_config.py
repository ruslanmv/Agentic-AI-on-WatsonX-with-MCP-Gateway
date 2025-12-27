"""Tests for configuration module."""

import pytest
from pydantic import ValidationError

from agentic_ai.core.config import Settings


def test_settings_defaults() -> None:
    """Test that settings have correct default values."""
    settings = Settings()

    assert settings.app_name == "Agentic AI on WatsonX with MCP Gateway"
    assert settings.app_version == "1.0.0"
    assert settings.debug is False
    assert settings.log_level == "INFO"
    assert settings.mcp_gateway_url == "http://localhost:8080"
    assert settings.max_concurrent_agents == 5
    assert settings.agent_timeout == 60


def test_settings_log_level_validation() -> None:
    """Test log level validation."""
    # Valid log levels
    for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        settings = Settings(log_level=level)
        assert settings.log_level == level

    # Invalid log level
    with pytest.raises(ValidationError):
        Settings(log_level="INVALID")


def test_settings_is_production() -> None:
    """Test production mode detection."""
    prod_settings = Settings(debug=False)
    assert prod_settings.is_production is True

    dev_settings = Settings(debug=True)
    assert dev_settings.is_production is False


def test_validate_watsonx_config() -> None:
    """Test WatsonX configuration validation."""
    # Complete config
    settings = Settings(
        watsonx_api_key="test-key",
        watsonx_project_id="test-project",
    )
    assert settings.validate_watsonx_config() is True

    # Incomplete config
    settings = Settings(watsonx_api_key="test-key")
    assert settings.validate_watsonx_config() is False


def test_validate_google_search_config() -> None:
    """Test Google Search configuration validation."""
    # Complete config
    settings = Settings(
        google_api_key="test-key",
        google_search_engine_id="test-engine",
    )
    assert settings.validate_google_search_config() is True

    # Incomplete config
    settings = Settings(google_api_key="test-key")
    assert settings.validate_google_search_config() is False
