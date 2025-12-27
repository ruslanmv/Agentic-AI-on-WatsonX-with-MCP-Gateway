"""
Wikipedia agent implementation.

This module provides an agent that retrieves encyclopedic knowledge
from Wikipedia using the MediaWiki API.
"""

from typing import Any, Optional

import httpx

from agentic_ai.agents.base import BaseAgent
from agentic_ai.core.exceptions import AgentError
from agentic_ai.core.logger import get_logger

logger = get_logger(__name__)


class WikipediaAgent(BaseAgent):
    """
    Agent for retrieving information from Wikipedia.

    This agent uses the MediaWiki API to search and retrieve content
    from Wikipedia articles.

    Attributes:
        name: Agent identifier
        description: Agent description
        client: HTTP client for API requests
        api_url: Wikipedia API endpoint URL
    """

    def __init__(
        self,
        name: str = "wikipedia-agent",
        description: str = "Retrieves encyclopedic knowledge from Wikipedia",
        language: str = "en",
    ) -> None:
        """
        Initialize the Wikipedia agent.

        Args:
            name: Agent identifier
            description: Agent description
            language: Wikipedia language code (default: 'en' for English)
        """
        super().__init__(name, description)
        self.language = language
        self.api_url = f"https://{language}.wikipedia.org/w/api.php"
        self.client: Optional[httpx.AsyncClient] = None

    async def initialize(self) -> None:
        """
        Initialize the HTTP client for API requests.

        Raises:
            AgentError: If initialization fails
        """
        try:
            self.client = httpx.AsyncClient(
                timeout=self.settings.agent_timeout,
                headers={"User-Agent": "AgenticAI/1.0 (https://ruslanmv.com)"},
            )
            self._initialized = True
            logger.info(f"Wikipedia agent '{self.name}' initialized successfully")
        except Exception as e:
            raise AgentError(
                f"Failed to initialize Wikipedia agent: {e}",
                details={"agent": self.name, "error": str(e)},
            ) from e

    async def execute(
        self,
        task: str,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Search Wikipedia and retrieve article content.

        Args:
            task: Search query or article title
            context: Optional context with parameters:
                - sentences: Number of sentences to extract (default: 5)
                - extract_plain: Return plain text instead of HTML (default: True)

        Returns:
            Dictionary containing:
                - query: The search query
                - title: Article title
                - extract: Article extract/summary
                - url: Full article URL
                - page_id: Wikipedia page ID

        Raises:
            AgentError: If search or retrieval fails
        """
        self._validate_initialized()

        if not self.client:
            raise AgentError("HTTP client not initialized", details={"agent": self.name})

        context = context or {}
        sentences = context.get("sentences", 5)
        extract_plain = context.get("extract_plain", True)

        logger.info(f"Searching Wikipedia for: '{task}'")

        try:
            # First, search for the article
            search_params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": task,
                "srlimit": 1,
            }

            response = await self.client.get(self.api_url, params=search_params)
            response.raise_for_status()
            search_data = response.json()

            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
                return {
                    "query": task,
                    "title": None,
                    "extract": None,
                    "url": None,
                    "page_id": None,
                    "error": "No results found",
                }

            page_title = search_results[0]["title"]
            page_id = search_results[0]["pageid"]

            # Get article extract
            extract_params = {
                "action": "query",
                "format": "json",
                "prop": "extracts|info",
                "exsentences": sentences,
                "explaintext": extract_plain,
                "inprop": "url",
                "titles": page_title,
            }

            response = await self.client.get(self.api_url, params=extract_params)
            response.raise_for_status()
            extract_data = response.json()

            pages = extract_data.get("query", {}).get("pages", {})
            page_data = pages.get(str(page_id), {})

            result = {
                "query": task,
                "title": page_data.get("title"),
                "extract": page_data.get("extract"),
                "url": page_data.get("fullurl"),
                "page_id": page_id,
            }

            logger.info(f"Retrieved Wikipedia article: '{result['title']}'")
            return result

        except httpx.HTTPStatusError as e:
            raise AgentError(
                f"Wikipedia API returned error: {e.response.status_code}",
                details={
                    "agent": self.name,
                    "query": task,
                    "status_code": e.response.status_code,
                },
            ) from e
        except Exception as e:
            raise AgentError(
                f"Failed to retrieve Wikipedia content: {e}",
                details={"agent": self.name, "query": task, "error": str(e)},
            ) from e

    async def cleanup(self) -> None:
        """Clean up HTTP client resources."""
        if self.client:
            await self.client.aclose()
            self.client = None
        await super().cleanup()
