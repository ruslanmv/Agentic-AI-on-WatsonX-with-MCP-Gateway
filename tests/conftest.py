"""
Pytest configuration and fixtures.

This module provides shared fixtures and configuration for all tests.
"""

import pytest

from agentic_ai.core.config import Settings


@pytest.fixture
def test_settings() -> Settings:
    """
    Provide test settings with safe defaults.

    Returns:
        Settings instance configured for testing
    """
    return Settings(
        debug=True,
        log_level="DEBUG",
        mcp_gateway_url="http://localhost:8080",
        watsonx_url="https://test.ml.cloud.ibm.com",
        watsonx_model="test-model",
        database_url="sqlite:///:memory:",
        max_concurrent_agents=2,
        agent_timeout=10,
    )


@pytest.fixture
def mock_google_credentials() -> dict[str, str]:
    """Provide mock Google Search credentials."""
    return {
        "api_key": "test-google-api-key",
        "search_engine_id": "test-search-engine-id",
    }


@pytest.fixture
def mock_watsonx_credentials() -> dict[str, str]:
    """Provide mock WatsonX credentials."""
    return {
        "api_key": "test-watsonx-api-key",
        "project_id": "test-project-id",
    }
