"""
Custom exception classes for the Agentic AI system.

This module defines a hierarchy of custom exceptions used throughout
the application for better error handling and debugging.
"""

from typing import Any, Optional


class AgenticAIError(Exception):
    """
    Base exception for all Agentic AI errors.

    All custom exceptions in this application inherit from this base class.

    Attributes:
        message: Human-readable error message
        details: Additional error details or context
    """

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            details: Optional dictionary containing additional error context
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ConfigurationError(AgenticAIError):
    """
    Exception raised for configuration-related errors.

    This exception is raised when there are issues with application
    configuration, such as missing required settings or invalid values.
    """

    pass


class AgentError(AgenticAIError):
    """
    Exception raised for agent-related errors.

    This exception is raised when an agent encounters an error during
    initialization, execution, or communication.
    """

    pass


class MCPError(AgenticAIError):
    """
    Exception raised for MCP (Model Context Protocol) related errors.

    This exception is raised when there are issues with MCP server
    communication, tool invocation, or protocol handling.
    """

    pass


class OrchestrationError(AgenticAIError):
    """
    Exception raised for orchestration-related errors.

    This exception is raised when the orchestrator encounters errors
    coordinating multiple agents or managing workflows.
    """

    pass


class ToolExecutionError(AgenticAIError):
    """
    Exception raised when a tool execution fails.

    This exception is raised when an MCP tool or external API
    call fails during execution.
    """

    pass


class ValidationError(AgenticAIError):
    """
    Exception raised for validation errors.

    This exception is raised when input validation fails or
    data doesn't meet expected schema requirements.
    """

    pass


class AuthenticationError(AgenticAIError):
    """
    Exception raised for authentication-related errors.

    This exception is raised when authentication with external
    services (WatsonX, MCP Gateway, etc.) fails.
    """

    pass


class NetworkError(AgenticAIError):
    """
    Exception raised for network-related errors.

    This exception is raised when network communication fails,
    including timeouts, connection errors, or HTTP errors.
    """

    pass
