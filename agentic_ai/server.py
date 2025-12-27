"""
FastAPI server for Agentic AI system.

This module provides a RESTful API server for interacting with the
multi-agent system via HTTP.
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agentic_ai import __version__
from agentic_ai.agents.google_search import GoogleSearchAgent
from agentic_ai.agents.watsonx_crafter import WatsonXCrafterAgent
from agentic_ai.agents.wikipedia import WikipediaAgent
from agentic_ai.core.config import get_settings
from agentic_ai.core.logger import LoggerConfig, get_logger
from agentic_ai.orchestrator.coordinator import AgentCoordinator
from agentic_ai.orchestrator.workflow import WorkflowEngine

# Initialize logger
settings = get_settings()
LoggerConfig.configure(log_level=settings.log_level, log_file=settings.get_log_file_path())
logger = get_logger(__name__)

# Global coordinator instance
coordinator: Optional[AgentCoordinator] = None
workflow_engine: Optional[WorkflowEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application lifespan events.

    This function initializes agents on startup and cleans them up on shutdown.
    """
    global coordinator, workflow_engine

    logger.info("Starting Agentic AI server...")

    # Initialize coordinator and agents
    coordinator = AgentCoordinator()

    try:
        coordinator.register_agent(GoogleSearchAgent())
    except Exception as e:
        logger.warning(f"Google Search agent not available: {e}")

    coordinator.register_agent(WikipediaAgent())
    coordinator.register_agent(WatsonXCrafterAgent())

    await coordinator.initialize_all()

    workflow_engine = WorkflowEngine(coordinator)

    logger.info("Agentic AI server started successfully")

    yield

    # Cleanup on shutdown
    logger.info("Shutting down Agentic AI server...")
    if coordinator:
        await coordinator.cleanup_all()
    logger.info("Server shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Agentic AI on WatsonX with MCP Gateway",
    description="Production-ready multi-agent AI system using IBM MCP Context Forge and WatsonX",
    version=__version__,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AgentTaskRequest(BaseModel):
    """Request model for agent task execution."""

    agent: str = Field(..., description="Name of the agent to execute")
    task: str = Field(..., description="Task description or query")
    context: Optional[dict[str, Any]] = Field(default=None, description="Optional task context")


class AgentTaskResponse(BaseModel):
    """Response model for agent task execution."""

    agent: str
    task: str
    result: dict[str, Any]
    status: str = "success"


class ResearchWorkflowRequest(BaseModel):
    """Request model for research workflow."""

    query: str = Field(..., description="Research query")
    num_search_results: int = Field(default=5, ge=1, le=10)
    wiki_sentences: int = Field(default=5, ge=1, le=10)
    report_max_tokens: int = Field(default=1500, ge=100, le=4000)


class ResearchWorkflowResponse(BaseModel):
    """Response model for research workflow."""

    query: str
    final_report: str
    metadata: dict[str, Any]
    status: str = "success"


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    agents: list[str]


# API Endpoints


@app.get("/", response_model=dict[str, str])
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": "Agentic AI on WatsonX with MCP Gateway",
        "version": __version__,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Coordinator not initialized",
        )

    return HealthResponse(
        status="healthy",
        version=__version__,
        agents=list(coordinator.agents.keys()),
    )


@app.get("/agents", response_model=dict[str, list[str]])
async def list_agents() -> dict[str, list[str]]:
    """List all registered agents."""
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Coordinator not initialized",
        )

    return {"agents": list(coordinator.agents.keys())}


@app.post("/execute", response_model=AgentTaskResponse)
async def execute_agent(request: AgentTaskRequest) -> AgentTaskResponse:
    """Execute a single agent task."""
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Coordinator not initialized",
        )

    try:
        result = await coordinator.execute_agent(
            agent_name=request.agent,
            task=request.task,
            context=request.context,
        )

        return AgentTaskResponse(
            agent=request.agent,
            task=request.task,
            result=result,
        )

    except Exception as e:
        logger.exception(f"Error executing agent {request.agent}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@app.post("/research", response_model=ResearchWorkflowResponse)
async def research_workflow(request: ResearchWorkflowRequest) -> ResearchWorkflowResponse:
    """Execute a complete research workflow."""
    if not workflow_engine:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Workflow engine not initialized",
        )

    try:
        result = await workflow_engine.execute_research_workflow(
            query=request.query,
            num_search_results=request.num_search_results,
            wiki_sentences=request.wiki_sentences,
            report_max_tokens=request.report_max_tokens,
        )

        return ResearchWorkflowResponse(
            query=result["query"],
            final_report=result["final_report"],
            metadata=result["metadata"],
        )

    except Exception as e:
        logger.exception(f"Error executing research workflow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False) -> None:
    """
    Run the FastAPI server.

    Args:
        host: Host to bind to
        port: Port to bind to
        reload: Enable auto-reload for development
    """
    import uvicorn

    uvicorn.run(
        "agentic_ai.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    run_server(reload=settings.debug)
