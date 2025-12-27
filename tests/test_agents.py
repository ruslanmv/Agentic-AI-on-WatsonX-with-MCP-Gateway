"""Tests for agent implementations."""

import pytest

from agentic_ai.agents.base import BaseAgent
from agentic_ai.agents.wikipedia import WikipediaAgent
from agentic_ai.core.exceptions import AgentError


class MockAgent(BaseAgent):
    """Mock agent for testing base class."""

    async def initialize(self) -> None:
        """Initialize the mock agent."""
        self._initialized = True

    async def execute(self, task: str, context: dict | None = None) -> dict:
        """Execute mock task."""
        return {"task": task, "result": "mock result"}


@pytest.mark.asyncio
async def test_base_agent_initialization() -> None:
    """Test base agent initialization."""
    agent = MockAgent(name="test-agent", description="Test agent")

    assert agent.name == "test-agent"
    assert agent.description == "Test agent"
    assert agent._initialized is False

    await agent.initialize()
    assert agent._initialized is True


@pytest.mark.asyncio
async def test_base_agent_context_manager() -> None:
    """Test base agent context manager protocol."""
    agent = MockAgent(name="test-agent", description="Test agent")

    assert agent._initialized is False

    async with agent as a:
        assert a._initialized is True
        assert a is agent

    assert agent._initialized is False


@pytest.mark.asyncio
async def test_base_agent_validate_initialized() -> None:
    """Test validation of agent initialization."""
    agent = MockAgent(name="test-agent", description="Test agent")

    with pytest.raises(AgentError, match="not initialized"):
        await agent.execute("test task")

    await agent.initialize()
    result = await agent.execute("test task")
    assert result["task"] == "test task"


@pytest.mark.asyncio
async def test_wikipedia_agent_initialization() -> None:
    """Test Wikipedia agent initialization."""
    agent = WikipediaAgent()

    assert agent.name == "wikipedia-agent"
    assert agent.language == "en"
    assert agent.client is None

    await agent.initialize()
    assert agent.client is not None
    assert agent._initialized is True

    await agent.cleanup()
    assert agent.client is None


def test_agent_repr() -> None:
    """Test agent string representation."""
    agent = MockAgent(name="test-agent", description="Test agent")
    assert repr(agent) == "MockAgent(name='test-agent')"
