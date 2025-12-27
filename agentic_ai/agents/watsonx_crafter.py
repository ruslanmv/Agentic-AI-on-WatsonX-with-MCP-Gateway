"""
WatsonX Crafter agent implementation.

This module provides an agent that uses IBM WatsonX AI to synthesize
information and create comprehensive reports.
"""

from typing import Any, Optional

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from agentic_ai.agents.base import BaseAgent
from agentic_ai.core.exceptions import AgentError, AuthenticationError, ConfigurationError
from agentic_ai.core.logger import get_logger

logger = get_logger(__name__)


class WatsonXCrafterAgent(BaseAgent):
    """
    Agent for synthesizing information using IBM WatsonX AI.

    This agent uses IBM's WatsonX foundation models to analyze information,
    synthesize insights, and create comprehensive reports.

    Attributes:
        name: Agent identifier
        description: Agent description
        model: WatsonX model instance
        model_id: WatsonX model identifier
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        url: Optional[str] = None,
        model_id: Optional[str] = None,
        name: str = "watsonx-crafter-agent",
        description: str = "Synthesizes information using IBM WatsonX AI",
    ) -> None:
        """
        Initialize the WatsonX Crafter agent.

        Args:
            api_key: IBM Cloud API key (optional, will use settings if not provided)
            project_id: WatsonX project ID (optional)
            url: WatsonX service URL (optional)
            model_id: Model identifier (optional)
            name: Agent identifier
            description: Agent description

        Raises:
            ConfigurationError: If required credentials are missing
        """
        super().__init__(name, description)

        # Get credentials from parameters or settings
        self.api_key = api_key or self.settings.watsonx_api_key
        self.project_id = project_id or self.settings.watsonx_project_id
        self.url = url or self.settings.watsonx_url
        self.model_id = model_id or self.settings.watsonx_model

        if not self.api_key or not self.project_id:
            raise ConfigurationError(
                "WatsonX credentials are required. "
                "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.",
                details={
                    "api_key_present": bool(self.api_key),
                    "project_id_present": bool(self.project_id),
                },
            )

        self.model: Optional[ModelInference] = None

    async def initialize(self) -> None:
        """
        Initialize the WatsonX model client.

        Raises:
            AgentError: If initialization fails
            AuthenticationError: If authentication fails
        """
        try:
            credentials = Credentials(url=self.url, api_key=self.api_key)

            self.model = ModelInference(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id,
            )

            self._initialized = True
            logger.info(
                f"WatsonX Crafter agent '{self.name}' initialized with model: {self.model_id}"
            )
        except Exception as e:
            error_msg = str(e).lower()
            if "auth" in error_msg or "credential" in error_msg or "unauthorized" in error_msg:
                raise AuthenticationError(
                    f"Failed to authenticate with WatsonX: {e}",
                    details={"agent": self.name, "error": str(e)},
                ) from e
            raise AgentError(
                f"Failed to initialize WatsonX agent: {e}",
                details={"agent": self.name, "error": str(e)},
            ) from e

    async def execute(
        self,
        task: str,
        context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Generate content using WatsonX AI.

        Args:
            task: The generation task or prompt
            context: Optional context with:
                - source_data: List of source materials to synthesize
                - max_tokens: Maximum tokens to generate (default: 1000)
                - temperature: Sampling temperature (default: 0.7)
                - stop_sequences: List of stop sequences

        Returns:
            Dictionary containing:
                - task: The original task
                - generated_text: Generated content
                - model_id: Model used for generation
                - input_tokens: Number of input tokens
                - generated_tokens: Number of generated tokens

        Raises:
            AgentError: If generation fails
        """
        self._validate_initialized()

        if not self.model:
            raise AgentError("WatsonX model not initialized", details={"agent": self.name})

        context = context or {}
        source_data = context.get("source_data", [])

        # Build the prompt
        prompt = self._build_prompt(task, source_data)

        # Generation parameters
        params = {
            "max_new_tokens": context.get("max_tokens", 1000),
            "temperature": context.get("temperature", 0.7),
            "top_p": context.get("top_p", 1.0),
            "top_k": context.get("top_k", 50),
        }

        stop_sequences = context.get("stop_sequences")
        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        logger.info(f"Generating content with WatsonX for task: '{task[:100]}...'")

        try:
            response = self.model.generate(prompt=prompt, params=params)

            generated_text = response.get("results", [{}])[0].get("generated_text", "")

            result = {
                "task": task,
                "generated_text": generated_text,
                "model_id": self.model_id,
                "input_tokens": response.get("results", [{}])[0].get("input_token_count", 0),
                "generated_tokens": response.get("results", [{}])[0].get(
                    "generated_token_count", 0
                ),
            }

            logger.info(
                f"Generated {result['generated_tokens']} tokens "
                f"using {result['input_tokens']} input tokens"
            )

            return result

        except Exception as e:
            raise AgentError(
                f"Failed to generate content with WatsonX: {e}",
                details={"agent": self.name, "task": task[:100], "error": str(e)},
            ) from e

    def _build_prompt(self, task: str, source_data: list[dict[str, Any]]) -> str:
        """
        Build a structured prompt from task and source data.

        Args:
            task: The generation task
            source_data: List of source materials

        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "You are a research assistant tasked with synthesizing information "
            "from multiple sources into a comprehensive, well-structured report.\n"
        ]

        if source_data:
            prompt_parts.append("\n## Source Materials:\n")
            for i, source in enumerate(source_data, 1):
                source_type = source.get("type", "source")
                content = source.get("content", "")
                prompt_parts.append(f"\n### Source {i} ({source_type}):\n{content}\n")

        prompt_parts.append(f"\n## Task:\n{task}\n")
        prompt_parts.append(
            "\n## Instructions:\n"
            "- Synthesize information from all provided sources\n"
            "- Create a well-structured, comprehensive report\n"
            "- Cite sources where appropriate\n"
            "- Ensure accuracy and coherence\n"
            "- Use clear, professional language\n"
            "\n## Report:\n"
        )

        return "".join(prompt_parts)

    async def cleanup(self) -> None:
        """Clean up WatsonX model resources."""
        self.model = None
        await super().cleanup()
