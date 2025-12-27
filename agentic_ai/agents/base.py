"""
Base agent class for all MCP agents.

This module provides the abstract base class that all agents inherit from,
defining the common interface and functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from agentic_ai.core.config import get_settings
from agentic_ai.core.exceptions import AgentError
from agentic_ai.core.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all MCP agents.

    This class provides the common interface and functionality that all
    agents must implement, including initialization, execution, and
    error handling.

    Attributes:
        name: Unique identifier for the agent
        description: Human-readable description of the agent's purpose
        settings: Application settings instance
    """

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize the base agent.

        Args:
            name: Unique identifier for the agent
            description: Human-readable description of the agent's purpose

        Raises:
            AgentError: If initialization fails
        """
        self.name = name
        self.description = description
        self.settings = get_settings()
        self._initialized = False
        logger.info(f"Initializing agent: {self.name}")

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the agent and its resources.

        This method must be implemented by subclasses to set up any
        required connections, load models, or prepare resources.

        Raises:
            AgentError: If initialization fails
        """
        pass

    @abstractmethod
    async def execute(self, task: str, context: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        """
        Execute a task using this agent.

        This method must be implemented by subclasses to define the
        agent's primary functionality.

        Args:
            task: The task description or query
            context: Optional context information for the task

        Returns:
            Dictionary containing the execution results

        Raises:
            AgentError: If execution fails
        """
        pass

    async def cleanup(self) -> None:
        """
        Clean up agent resources.

        This method can be overridden by subclasses to perform cleanup
        operations like closing connections or releasing resources.
        """
        logger.info(f"Cleaning up agent: {self.name}")
        self._initialized = False

    def _validate_initialized(self) -> None:
        """
        Validate that the agent has been initialized.

        Raises:
            AgentError: If the agent is not initialized
        """
        if not self._initialized:
            raise AgentError(
                f"Agent {self.name} is not initialized. Call initialize() first.",
                details={"agent": self.name},
            )

    async def __aenter__(self) -> "BaseAgent":
        """Support async context manager protocol."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Support async context manager protocol."""
        await self.cleanup()

    def __repr__(self) -> str:
        """Return string representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}')"
