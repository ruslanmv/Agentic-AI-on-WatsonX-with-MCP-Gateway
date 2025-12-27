"""
Workflow engine for complex multi-agent workflows.

This module provides a workflow engine that can execute predefined
multi-agent workflows with dependencies and data flow.
"""

from typing import Any, Callable, Optional

from agentic_ai.core.logger import get_logger
from agentic_ai.orchestrator.coordinator import AgentCoordinator

logger = get_logger(__name__)


class WorkflowEngine:
    """
    Engine for executing complex multi-agent workflows.

    This class provides a high-level interface for defining and executing
    workflows that involve multiple agents with dependencies and data flow.

    Attributes:
        coordinator: Agent coordinator instance
    """

    def __init__(self, coordinator: AgentCoordinator) -> None:
        """
        Initialize the workflow engine.

        Args:
            coordinator: Agent coordinator instance to use for execution
        """
        self.coordinator = coordinator
        logger.info("Workflow engine initialized")

    async def execute_research_workflow(
        self,
        query: str,
        num_search_results: int = 5,
        wiki_sentences: int = 5,
        report_max_tokens: int = 1500,
    ) -> dict[str, Any]:
        """
        Execute a research workflow using multiple agents.

        This workflow:
        1. Performs a Google search for the query
        2. Retrieves Wikipedia information about the query
        3. Synthesizes all information into a comprehensive report using WatsonX

        Args:
            query: Research query
            num_search_results: Number of search results to retrieve
            wiki_sentences: Number of Wikipedia sentences to retrieve
            report_max_tokens: Maximum tokens for the generated report

        Returns:
            Dictionary containing:
                - query: Original query
                - search_results: Google search results
                - wikipedia_data: Wikipedia article data
                - final_report: Synthesized report from WatsonX
                - metadata: Workflow execution metadata

        Raises:
            OrchestrationError: If workflow execution fails
        """
        logger.info(f"Starting research workflow for query: '{query}'")

        # Step 1 & 2: Execute Google search and Wikipedia retrieval in parallel
        parallel_tasks = [
            ("google-search-agent", query, {"num_results": num_search_results}),
            ("wikipedia-agent", query, {"sentences": wiki_sentences}),
        ]

        parallel_results = await self.coordinator.execute_parallel(parallel_tasks)
        search_results = parallel_results[0]
        wiki_data = parallel_results[1]

        logger.info("Parallel information gathering completed")

        # Step 3: Synthesize with WatsonX
        source_data = self._prepare_source_data(search_results, wiki_data)

        synthesis_task = (
            f"Create a comprehensive research report about: {query}\n\n"
            "Requirements:\n"
            "- Synthesize information from web search and Wikipedia sources\n"
            "- Structure the report with clear sections\n"
            "- Include key insights and findings\n"
            "- Maintain academic rigor and cite sources\n"
            "- Provide a conclusion with key takeaways"
        )

        synthesis_context = {
            "source_data": source_data,
            "max_tokens": report_max_tokens,
            "temperature": 0.7,
        }

        watsonx_result = await self.coordinator.execute_agent(
            "watsonx-crafter-agent",
            synthesis_task,
            synthesis_context,
        )

        logger.info("Research workflow completed successfully")

        return {
            "query": query,
            "search_results": search_results,
            "wikipedia_data": wiki_data,
            "final_report": watsonx_result.get("generated_text", ""),
            "metadata": {
                "num_search_results": len(search_results.get("results", [])),
                "wikipedia_title": wiki_data.get("title"),
                "report_tokens": watsonx_result.get("generated_tokens", 0),
                "total_input_tokens": watsonx_result.get("input_tokens", 0),
            },
        }

    def _prepare_source_data(
        self,
        search_results: dict[str, Any],
        wiki_data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Prepare source data for synthesis.

        Args:
            search_results: Google search results
            wiki_data: Wikipedia article data

        Returns:
            List of formatted source data dictionaries
        """
        sources = []

        # Add Wikipedia as first source if available
        if wiki_data.get("extract"):
            sources.append(
                {
                    "type": "Wikipedia",
                    "title": wiki_data.get("title"),
                    "url": wiki_data.get("url"),
                    "content": wiki_data.get("extract"),
                }
            )

        # Add search results
        for result in search_results.get("results", []):
            sources.append(
                {
                    "type": "Web Search",
                    "title": result.get("title"),
                    "url": result.get("link"),
                    "content": result.get("snippet"),
                }
            )

        return sources

    async def execute_custom_workflow(
        self,
        workflow_steps: list[dict[str, Any]],
        result_aggregator: Optional[Callable[[list[dict[str, Any]]], dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """
        Execute a custom workflow defined by steps.

        Args:
            workflow_steps: List of workflow step definitions, each containing:
                - agent: Agent name
                - task: Task description
                - context: Optional task context
                - depends_on: Optional list of step indices this depends on
                - parallel: Optional bool, whether this can run in parallel
            result_aggregator: Optional function to aggregate results

        Returns:
            Aggregated workflow results

        Raises:
            OrchestrationError: If workflow execution fails
        """
        logger.info(f"Starting custom workflow with {len(workflow_steps)} steps")

        results: list[dict[str, Any]] = []

        # Simple sequential execution for now
        # TODO: Implement proper dependency resolution and parallel execution
        for i, step in enumerate(workflow_steps):
            agent_name = step["agent"]
            task = step["task"]
            context = step.get("context", {})

            # Inject results from dependencies if specified
            depends_on = step.get("depends_on", [])
            if depends_on:
                context["previous_results"] = [results[idx] for idx in depends_on]

            logger.info(f"Executing workflow step {i + 1}/{len(workflow_steps)}: {agent_name}")

            result = await self.coordinator.execute_agent(agent_name, task, context)
            results.append(result)

        logger.info("Custom workflow completed")

        # Aggregate results if aggregator provided
        if result_aggregator:
            return result_aggregator(results)

        return {"steps": results, "total_steps": len(workflow_steps)}
