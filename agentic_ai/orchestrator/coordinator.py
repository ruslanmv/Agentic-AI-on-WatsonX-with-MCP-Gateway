"""
Multi-agent coordinator for orchestrating agent execution.

This module provides the coordinator that manages multiple agents,
handling their lifecycle, execution, and result aggregation.
"""

import asyncio
from typing import Any, Optional

from agentic_ai.agents.base import BaseAgent
from agentic_ai.core.config import get_settings
from agentic_ai.core.exceptions import OrchestrationError
from agentic_ai.core.logger import get_logger

logger = get_logger(__name__)


class AgentCoordinator:
    """
    Coordinator for managing and executing multiple agents.

    This class handles the orchestration of multiple agents, managing
    their lifecycle, parallel execution, and result aggregation.

    Attributes:
        agents: Dictionary of registered agents by name
        settings: Application settings instance
        max_concurrent: Maximum number of agents to run concurrently
    """

    def __init__(self, max_concurrent: Optional[int] = None) -> None:
        """
        Initialize the agent coordinator.

        Args:
            max_concurrent: Maximum concurrent agents (uses settings if not provided)
        """
        self.agents: dict[str, BaseAgent] = {}
        self.settings = get_settings()
        self.max_concurrent = max_concurrent or self.settings.max_concurrent_agents
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        logger.info(f"Agent coordinator initialized with max_concurrent={self.max_concurrent}")

    def register_agent(self, agent: BaseAgent) -> None:
        """
        Register an agent with the coordinator.

        Args:
            agent: Agent instance to register

        Raises:
            OrchestrationError: If agent name is already registered
        """
        if agent.name in self.agents:
            raise OrchestrationError(
                f"Agent with name '{agent.name}' is already registered",
                details={"agent": agent.name},
            )

        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    def unregister_agent(self, name: str) -> None:
        """
        Unregister an agent from the coordinator.

        Args:
            name: Name of the agent to unregister
        """
        if name in self.agents:
            del self.agents[name]
            logger.info(f"Unregistered agent: {name}")

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """
        Get a registered agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(name)

    async def initialize_all(self) -> None:
        """
        Initialize all registered agents.

        Raises:
            OrchestrationError: If initialization fails for any agent
        """
        logger.info(f"Initializing {len(self.agents)} agents...")

        try:
            await asyncio.gather(
                *[agent.initialize() for agent in self.agents.values()],
                return_exceptions=False,
            )
            logger.info("All agents initialized successfully")
        except Exception as e:
            raise OrchestrationError(
                f"Failed to initialize agents: {e}",
                details={"error": str(e)},
            ) from e

    async def cleanup_all(self) -> None:
        """Clean up all registered agents."""
        logger.info("Cleaning up all agents...")

        await asyncio.gather(
            *[agent.cleanup() for agent in self.agents.values()],
            return_exceptions=True,  # Don't fail if some cleanups fail
        )

        logger.info("All agents cleaned up")

    async def execute_agent(
        self,
        agent_name: str,
        task: str,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Execute a single agent with the given task.

        Args:
            agent_name: Name of the agent to execute
            task: Task description
            context: Optional task context

        Returns:
            Agent execution results

        Raises:
            OrchestrationError: If agent is not found or execution fails
        """
        agent = self.get_agent(agent_name)
        if not agent:
            raise OrchestrationError(
                f"Agent '{agent_name}' not found",
                details={"agent": agent_name, "registered_agents": list(self.agents.keys())},
            )

        logger.info(f"Executing agent '{agent_name}' with task: '{task[:100]}...'")

        async with self._semaphore:
            try:
                result = await agent.execute(task, context)
                logger.info(f"Agent '{agent_name}' completed successfully")
                return result
            except Exception as e:
                raise OrchestrationError(
                    f"Agent '{agent_name}' execution failed: {e}",
                    details={"agent": agent_name, "task": task, "error": str(e)},
                ) from e

    async def execute_parallel(
        self,
        tasks: list[tuple[str, str, Optional[dict[str, Any]]]],
    ) -> list[dict[str, Any]]:
        """
        Execute multiple agents in parallel.

        Args:
            tasks: List of tuples containing (agent_name, task, context)

        Returns:
            List of results from each agent execution

        Raises:
            OrchestrationError: If any execution fails
        """
        logger.info(f"Executing {len(tasks)} agents in parallel...")

        try:
            results = await asyncio.gather(
                *[self.execute_agent(agent_name, task, context) for agent_name, task, context in tasks],
                return_exceptions=False,
            )

            logger.info(f"All {len(tasks)} parallel executions completed")
            return list(results)

        except Exception as e:
            raise OrchestrationError(
                f"Parallel execution failed: {e}",
                details={"num_tasks": len(tasks), "error": str(e)},
            ) from e

    async def execute_sequential(
        self,
        tasks: list[tuple[str, str, Optional[dict[str, Any]]]],
    ) -> list[dict[str, Any]]:
        """
        Execute multiple agents sequentially.

        Args:
            tasks: List of tuples containing (agent_name, task, context)

        Returns:
            List of results from each agent execution in order

        Raises:
            OrchestrationError: If any execution fails
        """
        logger.info(f"Executing {len(tasks)} agents sequentially...")

        results = []
        for i, (agent_name, task, context) in enumerate(tasks, 1):
            logger.info(f"Sequential execution {i}/{len(tasks)}: {agent_name}")
            result = await self.execute_agent(agent_name, task, context)
            results.append(result)

        logger.info(f"All {len(tasks)} sequential executions completed")
        return results

    async def __aenter__(self) -> "AgentCoordinator":
        """Support async context manager protocol."""
        await self.initialize_all()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Support async context manager protocol."""
        await self.cleanup_all()

    def __repr__(self) -> str:
        """Return string representation of the coordinator."""
        return f"AgentCoordinator(agents={list(self.agents.keys())}, max_concurrent={self.max_concurrent})"
