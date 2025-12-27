"""
Command-line interface for Agentic AI.

This module provides a rich CLI for interacting with the multi-agent system.
"""

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from agentic_ai import __version__
from agentic_ai.agents.google_search import GoogleSearchAgent
from agentic_ai.agents.watsonx_crafter import WatsonXCrafterAgent
from agentic_ai.agents.wikipedia import WikipediaAgent
from agentic_ai.core.config import get_settings
from agentic_ai.core.logger import LoggerConfig, get_logger
from agentic_ai.orchestrator.coordinator import AgentCoordinator
from agentic_ai.orchestrator.workflow import WorkflowEngine

app = typer.Typer(
    name="agentic-ai",
    help="Agentic AI on WatsonX with MCP Gateway - Multi-agent AI System",
    add_completion=False,
)
console = Console()
logger = get_logger(__name__)


def version_callback(value: bool) -> None:
    """Display version information."""
    if value:
        console.print(f"[bold blue]Agentic AI[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Agentic AI on WatsonX with MCP Gateway."""
    pass


@app.command()
def config() -> None:
    """Display current configuration."""
    settings = get_settings()

    table = Table(title="Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    # Application settings
    table.add_row("App Name", settings.app_name)
    table.add_row("Version", settings.app_version)
    table.add_row("Debug Mode", str(settings.debug))
    table.add_row("Log Level", settings.log_level)

    # MCP Gateway
    table.add_row("MCP Gateway URL", settings.mcp_gateway_url)
    table.add_row("MCP Gateway API Key", "***" if settings.mcp_gateway_api_key else "Not Set")

    # WatsonX
    table.add_row("WatsonX URL", settings.watsonx_url)
    table.add_row("WatsonX API Key", "***" if settings.watsonx_api_key else "Not Set")
    table.add_row("WatsonX Project ID", settings.watsonx_project_id or "Not Set")
    table.add_row("WatsonX Model", settings.watsonx_model)

    # Agent settings
    table.add_row("Max Concurrent Agents", str(settings.max_concurrent_agents))
    table.add_row("Agent Timeout", f"{settings.agent_timeout}s")

    console.print(table)


@app.command()
def demo(
    query: str = typer.Argument(
        "Artificial Intelligence and Machine Learning",
        help="Research query to demonstrate the workflow",
    ),
) -> None:
    """Run a demonstration of the multi-agent research workflow."""
    LoggerConfig.configure(log_level="INFO")

    console.print(
        Panel.fit(
            "[bold blue]Agentic AI Research Workflow Demo[/bold blue]\n"
            f"[yellow]Query:[/yellow] {query}",
            border_style="blue",
        )
    )

    asyncio.run(_run_demo(query))


async def _run_demo(query: str) -> None:
    """Execute the demo workflow."""
    settings = get_settings()

    # Validate configuration
    if not settings.validate_watsonx_config():
        console.print(
            "[bold red]Error:[/bold red] WatsonX credentials not configured.\n"
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables."
        )
        raise typer.Exit(1)

    try:
        # Initialize coordinator
        coordinator = AgentCoordinator()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Register agents
            task = progress.add_task("[cyan]Registering agents...", total=None)

            try:
                google_agent = GoogleSearchAgent()
                coordinator.register_agent(google_agent)
            except Exception as e:
                logger.warning(f"Google Search agent not available: {e}")
                console.print("[yellow]Warning:[/yellow] Google Search agent not available (missing credentials)")

            coordinator.register_agent(WikipediaAgent())
            coordinator.register_agent(WatsonXCrafterAgent())

            progress.update(task, description="[green]Agents registered successfully")

            # Initialize agents
            progress.update(task, description="[cyan]Initializing agents...")
            await coordinator.initialize_all()
            progress.update(task, description="[green]Agents initialized")

            # Execute workflow
            progress.update(task, description="[cyan]Executing research workflow...")

            workflow = WorkflowEngine(coordinator)
            result = await workflow.execute_research_workflow(
                query=query,
                num_search_results=5,
                wiki_sentences=5,
                report_max_tokens=1500,
            )

            progress.update(task, description="[green]Workflow completed!")

        # Display results
        console.print("\n")
        console.print(Panel("[bold green]Research Report[/bold green]", border_style="green"))
        console.print(result["final_report"])
        console.print("\n")

        # Display metadata
        metadata_table = Table(title="Workflow Metadata", show_header=False)
        metadata_table.add_column("Key", style="cyan")
        metadata_table.add_column("Value", style="green")

        metadata = result["metadata"]
        metadata_table.add_row("Search Results", str(metadata["num_search_results"]))
        metadata_table.add_row("Wikipedia Article", metadata.get("wikipedia_title") or "N/A")
        metadata_table.add_row("Report Tokens", str(metadata["report_tokens"]))
        metadata_table.add_row("Input Tokens", str(metadata["total_input_tokens"]))

        console.print(metadata_table)

        # Cleanup
        await coordinator.cleanup_all()

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        logger.exception(e)
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    num_results: int = typer.Option(5, "--num", "-n", help="Number of results"),
) -> None:
    """Perform a Google search using the search agent."""
    LoggerConfig.configure(log_level="INFO")

    asyncio.run(_run_search(query, num_results))


async def _run_search(query: str, num_results: int) -> None:
    """Execute a search."""
    try:
        async with GoogleSearchAgent() as agent:
            result = await agent.execute(query, {"num_results": num_results})

            console.print(f"\n[bold]Search Results for:[/bold] {query}\n")

            for i, item in enumerate(result["results"], 1):
                console.print(f"[bold cyan]{i}. {item['title']}[/bold cyan]")
                console.print(f"   [blue]{item['link']}[/blue]")
                console.print(f"   {item['snippet']}\n")

            console.print(f"[dim]Total results: {result['total_results']:,}[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def wiki(
    query: str = typer.Argument(..., help="Wikipedia query"),
    sentences: int = typer.Option(5, "--sentences", "-s", help="Number of sentences"),
) -> None:
    """Retrieve information from Wikipedia."""
    LoggerConfig.configure(log_level="INFO")

    asyncio.run(_run_wiki(query, sentences))


async def _run_wiki(query: str, sentences: int) -> None:
    """Execute a Wikipedia search."""
    try:
        async with WikipediaAgent() as agent:
            result = await agent.execute(query, {"sentences": sentences})

            if result.get("title"):
                console.print(Panel(f"[bold]{result['title']}[/bold]", border_style="blue"))
                console.print(f"\n{result['extract']}\n")
                console.print(f"[dim]Source: {result['url']}[/dim]")
            else:
                console.print(f"[yellow]No Wikipedia article found for: {query}[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)


def main_cli() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main_cli()
