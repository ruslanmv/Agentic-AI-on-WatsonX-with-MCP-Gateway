"""
Agentic AI on WatsonX with MCP Gateway.

A production-ready multi-agent AI system using IBM MCP Context Forge and WatsonX.

This package provides a comprehensive framework for building sophisticated
multi-agent AI systems using the Model Context Protocol (MCP) and IBM's
WatsonX AI platform.

Author: Ruslan Magana
Website: https://ruslanmv.com
License: Apache-2.0
"""

__version__ = "1.0.0"
__author__ = "Ruslan Magana"
__email__ = "info@ruslanmv.com"
__license__ = "Apache-2.0"

from agentic_ai.core.config import Settings, get_settings
from agentic_ai.core.exceptions import (
    AgenticAIError,
    AgentError,
    ConfigurationError,
    MCPError,
)
from agentic_ai.core.logger import get_logger

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "Settings",
    "get_settings",
    "get_logger",
    "AgenticAIError",
    "AgentError",
    "ConfigurationError",
    "MCPError",
]
