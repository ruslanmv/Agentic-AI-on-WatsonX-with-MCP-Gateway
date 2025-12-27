"""Tests for exception classes."""

from agentic_ai.core.exceptions import (
    AgenticAIError,
    AgentError,
    AuthenticationError,
    ConfigurationError,
    MCPError,
    NetworkError,
    OrchestrationError,
    ToolExecutionError,
    ValidationError,
)


def test_base_exception() -> None:
    """Test base exception class."""
    error = AgenticAIError("Test error", details={"key": "value"})

    assert str(error) == "Test error | Details: {'key': 'value'}"
    assert error.message == "Test error"
    assert error.details == {"key": "value"}


def test_base_exception_without_details() -> None:
    """Test base exception without details."""
    error = AgenticAIError("Test error")

    assert str(error) == "Test error"
    assert error.details == {}


def test_configuration_error() -> None:
    """Test configuration error."""
    error = ConfigurationError("Config missing")
    assert isinstance(error, AgenticAIError)
    assert str(error) == "Config missing"


def test_agent_error() -> None:
    """Test agent error."""
    error = AgentError("Agent failed", details={"agent": "test-agent"})
    assert isinstance(error, AgenticAIError)
    assert error.details["agent"] == "test-agent"


def test_mcp_error() -> None:
    """Test MCP error."""
    error = MCPError("MCP connection failed")
    assert isinstance(error, AgenticAIError)


def test_orchestration_error() -> None:
    """Test orchestration error."""
    error = OrchestrationError("Orchestration failed")
    assert isinstance(error, AgenticAIError)


def test_tool_execution_error() -> None:
    """Test tool execution error."""
    error = ToolExecutionError("Tool failed")
    assert isinstance(error, AgenticAIError)


def test_validation_error() -> None:
    """Test validation error."""
    error = ValidationError("Invalid input")
    assert isinstance(error, AgenticAIError)


def test_authentication_error() -> None:
    """Test authentication error."""
    error = AuthenticationError("Auth failed")
    assert isinstance(error, AgenticAIError)


def test_network_error() -> None:
    """Test network error."""
    error = NetworkError("Network timeout")
    assert isinstance(error, AgenticAIError)
