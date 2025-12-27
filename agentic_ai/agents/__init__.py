"""
MCP Agent implementations for various specialized tasks.

This module provides concrete implementations of MCP agents for:
- Google Search
- Wikipedia knowledge retrieval
- WatsonX AI-powered content generation
"""

from agentic_ai.agents.base import BaseAgent
from agentic_ai.agents.google_search import GoogleSearchAgent
from agentic_ai.agents.watsonx_crafter import WatsonXCrafterAgent
from agentic_ai.agents.wikipedia import WikipediaAgent

__all__ = [
    "BaseAgent",
    "GoogleSearchAgent",
    "WikipediaAgent",
    "WatsonXCrafterAgent",
]
