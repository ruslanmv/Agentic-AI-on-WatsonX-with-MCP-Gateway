"""Tests for agent coordinator."""

import pytest

from agentic_ai.agents.base import BaseAgent
from agentic_ai.core.exceptions import OrchestrationError
from agentic_ai.orchestrator.coordinator import AgentCoordinator


class MockAgent(BaseAgent):
    """Mock agent for testing."""

    async def initialize(self) -> None:
        """Initialize the mock agent."""
        self._initialized = True

    async def execute(self, task: str, context: dict | None = None) -> dict:
        """Execute mock task."""
        return {"agent": self.name, "task": task, "result": "success"}


@pytest.mark.asyncio
async def test_coordinator_initialization() -> None:
    """Test coordinator initialization."""
    coordinator = AgentCoordinator(max_concurrent=3)

    assert coordinator.max_concurrent == 3
    assert len(coordinator.agents) == 0


@pytest.mark.asyncio
async def test_register_agent() -> None:
    """Test agent registration."""
    coordinator = AgentCoordinator()
    agent = MockAgent(name="test-agent", description="Test")

    coordinator.register_agent(agent)

    assert "test-agent" in coordinator.agents
    assert coordinator.get_agent("test-agent") is agent


@pytest.mark.asyncio
async def test_register_duplicate_agent() -> None:
    """Test registering duplicate agent raises error."""
    coordinator = AgentCoordinator()
    agent1 = MockAgent(name="test-agent", description="Test 1")
    agent2 = MockAgent(name="test-agent", description="Test 2")

    coordinator.register_agent(agent1)

    with pytest.raises(OrchestrationError, match="already registered"):
        coordinator.register_agent(agent2)


@pytest.mark.asyncio
async def test_unregister_agent() -> None:
    """Test agent unregistration."""
    coordinator = AgentCoordinator()
    agent = MockAgent(name="test-agent", description="Test")

    coordinator.register_agent(agent)
    assert "test-agent" in coordinator.agents

    coordinator.unregister_agent("test-agent")
    assert "test-agent" not in coordinator.agents


@pytest.mark.asyncio
async def test_initialize_all() -> None:
    """Test initializing all agents."""
    coordinator = AgentCoordinator()

    agent1 = MockAgent(name="agent-1", description="Agent 1")
    agent2 = MockAgent(name="agent-2", description="Agent 2")

    coordinator.register_agent(agent1)
    coordinator.register_agent(agent2)

    await coordinator.initialize_all()

    assert agent1._initialized is True
    assert agent2._initialized is True


@pytest.mark.asyncio
async def test_execute_agent() -> None:
    """Test executing a single agent."""
    coordinator = AgentCoordinator()
    agent = MockAgent(name="test-agent", description="Test")

    coordinator.register_agent(agent)
    await coordinator.initialize_all()

    result = await coordinator.execute_agent("test-agent", "test task")

    assert result["agent"] == "test-agent"
    assert result["task"] == "test task"
    assert result["result"] == "success"


@pytest.mark.asyncio
async def test_execute_nonexistent_agent() -> None:
    """Test executing nonexistent agent raises error."""
    coordinator = AgentCoordinator()

    with pytest.raises(OrchestrationError, match="not found"):
        await coordinator.execute_agent("nonexistent", "test task")


@pytest.mark.asyncio
async def test_execute_parallel() -> None:
    """Test parallel agent execution."""
    coordinator = AgentCoordinator()

    agent1 = MockAgent(name="agent-1", description="Agent 1")
    agent2 = MockAgent(name="agent-2", description="Agent 2")

    coordinator.register_agent(agent1)
    coordinator.register_agent(agent2)
    await coordinator.initialize_all()

    tasks = [
        ("agent-1", "task 1", None),
        ("agent-2", "task 2", None),
    ]

    results = await coordinator.execute_parallel(tasks)

    assert len(results) == 2
    assert results[0]["agent"] == "agent-1"
    assert results[1]["agent"] == "agent-2"


@pytest.mark.asyncio
async def test_execute_sequential() -> None:
    """Test sequential agent execution."""
    coordinator = AgentCoordinator()

    agent1 = MockAgent(name="agent-1", description="Agent 1")
    agent2 = MockAgent(name="agent-2", description="Agent 2")

    coordinator.register_agent(agent1)
    coordinator.register_agent(agent2)
    await coordinator.initialize_all()

    tasks = [
        ("agent-1", "task 1", None),
        ("agent-2", "task 2", None),
    ]

    results = await coordinator.execute_sequential(tasks)

    assert len(results) == 2
    assert results[0]["agent"] == "agent-1"
    assert results[1]["agent"] == "agent-2"


@pytest.mark.asyncio
async def test_coordinator_context_manager() -> None:
    """Test coordinator context manager protocol."""
    coordinator = AgentCoordinator()
    agent = MockAgent(name="test-agent", description="Test")

    coordinator.register_agent(agent)

    assert agent._initialized is False

    async with coordinator:
        assert agent._initialized is True

    assert agent._initialized is False
