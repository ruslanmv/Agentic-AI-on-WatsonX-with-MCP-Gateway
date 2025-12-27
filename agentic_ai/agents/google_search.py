"""
Google Search agent implementation.

This module provides an agent that performs web searches using the Google
Custom Search API and returns relevant results.
"""

from typing import Any, Optional

import httpx

from agentic_ai.agents.base import BaseAgent
from agentic_ai.core.exceptions import AgentError, ConfigurationError
from agentic_ai.core.logger import get_logger

logger = get_logger(__name__)


class GoogleSearchAgent(BaseAgent):
    """
    Agent for performing Google searches.

    This agent uses the Google Custom Search API to perform web searches
    and retrieve relevant articles and information.

    Attributes:
        name: Agent identifier
        description: Agent description
        api_key: Google API key
        search_engine_id: Google Custom Search Engine ID
        client: HTTP client for API requests
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        search_engine_id: Optional[str] = None,
        name: str = "google-search-agent",
        description: str = "Performs web searches using Google Custom Search API",
    ) -> None:
        """
        Initialize the Google Search agent.

        Args:
            api_key: Google API key (optional, will use settings if not provided)
            search_engine_id: Custom Search Engine ID (optional)
            name: Agent identifier
            description: Agent description

        Raises:
            ConfigurationError: If required credentials are missing
        """
        super().__init__(name, description)

        # Get credentials from parameters or settings
        self.api_key = api_key or self.settings.google_api_key
        self.search_engine_id = search_engine_id or self.settings.google_search_engine_id

        if not self.api_key or not self.search_engine_id:
            raise ConfigurationError(
                "Google Search API credentials are required. "
                "Set GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID environment variables.",
                details={
                    "api_key_present": bool(self.api_key),
                    "search_engine_id_present": bool(self.search_engine_id),
                },
            )

        self.client: Optional[httpx.AsyncClient] = None
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    async def initialize(self) -> None:
        """
        Initialize the HTTP client for API requests.

        Raises:
            AgentError: If initialization fails
        """
        try:
            self.client = httpx.AsyncClient(timeout=self.settings.agent_timeout)
            self._initialized = True
            logger.info(f"Google Search agent '{self.name}' initialized successfully")
        except Exception as e:
            raise AgentError(
                f"Failed to initialize Google Search agent: {e}",
                details={"agent": self.name, "error": str(e)},
            ) from e

    async def execute(
        self,
        task: str,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Perform a Google search.

        Args:
            task: Search query string
            context: Optional context with search parameters (num_results, etc.)

        Returns:
            Dictionary containing search results with keys:
                - query: The search query
                - results: List of search result items
                - total_results: Estimated total number of results

        Raises:
            AgentError: If search fails
        """
        self._validate_initialized()

        if not self.client:
            raise AgentError("HTTP client not initialized", details={"agent": self.name})

        context = context or {}
        num_results = context.get("num_results", 10)

        logger.info(f"Executing Google search: '{task}'")

        try:
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": task,
                "num": min(num_results, 10),  # Google API max is 10 per request
            }

            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()

            results = []
            for item in data.get("items", []):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "display_link": item.get("displayLink", ""),
                    }
                )

            search_info = data.get("searchInformation", {})
            total_results = search_info.get("totalResults", "0")

            logger.info(
                f"Google search completed: {len(results)} results for '{task}'"
            )

            return {
                "query": task,
                "results": results,
                "total_results": int(total_results),
                "search_time": search_info.get("searchTime", 0),
            }

        except httpx.HTTPStatusError as e:
            raise AgentError(
                f"Google Search API returned error: {e.response.status_code}",
                details={
                    "agent": self.name,
                    "query": task,
                    "status_code": e.response.status_code,
                    "response": e.response.text,
                },
            ) from e
        except Exception as e:
            raise AgentError(
                f"Failed to execute Google search: {e}",
                details={"agent": self.name, "query": task, "error": str(e)},
            ) from e

    async def cleanup(self) -> None:
        """Clean up HTTP client resources."""
        if self.client:
            await self.client.aclose()
            self.client = None
        await super().cleanup()
