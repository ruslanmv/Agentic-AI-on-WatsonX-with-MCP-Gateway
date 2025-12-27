"""
Application configuration management.

This module provides configuration management using pydantic-settings,
supporting environment variables, .env files, and type validation.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with validation and environment variable support.

    This class defines all application configuration settings with type hints,
    validation, and default values. Settings can be provided via environment
    variables or a .env file.

    Attributes:
        app_name: Application name
        app_version: Application version
        debug: Enable debug mode
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)

        # MCP Gateway Configuration
        mcp_gateway_url: URL of the MCP Context Forge Gateway
        mcp_gateway_api_key: API key for MCP Gateway authentication
        mcp_gateway_timeout: Request timeout in seconds

        # WatsonX Configuration
        watsonx_api_key: IBM WatsonX API key
        watsonx_project_id: IBM WatsonX project ID
        watsonx_url: IBM WatsonX service URL
        watsonx_model: Model to use for generation

        # Database Configuration
        database_url: SQLAlchemy database URL
        redis_url: Redis connection URL (optional)

        # Agent Configuration
        max_concurrent_agents: Maximum number of agents running concurrently
        agent_timeout: Default timeout for agent operations in seconds
        max_retries: Maximum number of retries for failed operations
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    app_name: str = Field(default="Agentic AI on WatsonX with MCP Gateway")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    log_file: Optional[Path] = Field(default=None)

    # MCP Gateway Configuration
    mcp_gateway_url: str = Field(
        default="http://localhost:8080",
        description="URL of the MCP Context Forge Gateway",
    )
    mcp_gateway_api_key: Optional[str] = Field(
        default=None,
        description="API key for MCP Gateway authentication",
    )
    mcp_gateway_timeout: int = Field(default=30, ge=1, le=300)

    # WatsonX Configuration
    watsonx_api_key: Optional[str] = Field(
        default=None,
        description="IBM WatsonX API key",
    )
    watsonx_project_id: Optional[str] = Field(
        default=None,
        description="IBM WatsonX project ID",
    )
    watsonx_url: str = Field(
        default="https://us-south.ml.cloud.ibm.com",
        description="IBM WatsonX service URL",
    )
    watsonx_model: str = Field(
        default="ibm/granite-13b-chat-v2",
        description="Model to use for generation",
    )

    # Database Configuration
    database_url: str = Field(
        default="sqlite:///./agentic_ai.db",
        description="SQLAlchemy database URL",
    )
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis connection URL for caching",
    )

    # Agent Configuration
    max_concurrent_agents: int = Field(default=5, ge=1, le=20)
    agent_timeout: int = Field(default=60, ge=1, le=600)
    max_retries: int = Field(default=3, ge=0, le=10)

    # Google Search Configuration (Optional)
    google_api_key: Optional[str] = Field(default=None)
    google_search_engine_id: Optional[str] = Field(default=None)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard logging levels."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v_upper

    @field_validator("log_file", mode="before")
    @classmethod
    def validate_log_file(cls, v: Optional[str]) -> Optional[Path]:
        """Convert log file string to Path if provided."""
        if v is None or v == "":
            return None
        return Path(v)

    def get_log_file_path(self) -> Optional[Path]:
        """
        Get the log file path, creating parent directories if needed.

        Returns:
            Path object for the log file, or None if not configured
        """
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            return self.log_file
        return None

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug

    def validate_watsonx_config(self) -> bool:
        """
        Validate WatsonX configuration is complete.

        Returns:
            True if WatsonX is properly configured, False otherwise
        """
        return bool(self.watsonx_api_key and self.watsonx_project_id)

    def validate_google_search_config(self) -> bool:
        """
        Validate Google Search configuration is complete.

        Returns:
            True if Google Search is properly configured, False otherwise
        """
        return bool(self.google_api_key and self.google_search_engine_id)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings instance.

    This function returns a singleton settings instance, ensuring
    settings are loaded only once during application lifecycle.

    Returns:
        Settings instance with validated configuration

    Example:
        >>> settings = get_settings()
        >>> print(settings.app_name)
        Agentic AI on WatsonX with MCP Gateway
    """
    return Settings()
