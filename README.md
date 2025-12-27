# Agentic AI on WatsonX with MCP Gateway

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-managed-blueviolet)](https://github.com/astral-sh/uv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready, commercial-grade multi-agent AI system leveraging IBM's MCP Context Forge Gateway and WatsonX AI platform. This framework enables sophisticated agent-based workflows for research, analysis, and content generation.

**Author:** Ruslan Magana
**Website:** [ruslanmv.com](https://ruslanmv.com)
**License:** Apache 2.0

---

## 📋 Table of Contents

- [About](#about)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI](#cli)
  - [REST API](#rest-api)
  - [Python API](#python-api)
- [Agents](#agents)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 About

This project demonstrates enterprise-grade multi-agent AI architecture using:

- **IBM MCP Context Forge Gateway**: A federated gateway for MCP (Model Context Protocol) servers and REST services
- **IBM WatsonX AI**: Advanced foundation models for content generation and synthesis
- **Multi-Agent Orchestration**: Coordinated execution of specialized agents for complex workflows

### What is the Model Context Protocol (MCP)?

MCP is an open standard that provides a unified way for AI applications to interact with external tools and services. Think of it as "USB-C for AI tools" - a standardized interface that enables:

- **Interoperability**: Tools work across different AI frameworks
- **Security**: Controlled, authenticated access to resources
- **Scalability**: Easy addition of new capabilities without framework changes

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Client Applications                        │
│            (CLI, REST API, Python SDK)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Agent Coordinator                               │
│  • Manages agent lifecycle                                   │
│  • Handles parallel/sequential execution                     │
│  • Aggregates results                                        │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
┌──────▼────┐  ┌──────▼────┐  ┌─────▼──────┐
│  Google   │  │ Wikipedia │  │  WatsonX   │
│  Search   │  │   Agent   │  │  Crafter   │
│  Agent    │  │           │  │   Agent    │
└───────────┘  └───────────┘  └────────────┘
       │              │              │
       └──────────────┴──────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         IBM MCP Context Forge Gateway                        │
│  • Protocol translation                                      │
│  • Authentication & security                                 │
│  • Federation & caching                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Core Capabilities

- **Multi-Agent Orchestration**: Coordinate multiple specialized agents for complex tasks
- **Parallel & Sequential Execution**: Optimize workflow performance
- **Type-Safe Configuration**: Pydantic-based settings with validation
- **Production-Ready Logging**: Structured logging with rotation and filtering
- **Comprehensive Testing**: Full test coverage with pytest
- **Docker Support**: Containerized deployment with docker-compose
- **REST API**: FastAPI-based HTTP interface
- **Rich CLI**: Interactive command-line interface with beautiful output

### Included Agents

1. **Google Search Agent**
   - Web search capabilities using Google Custom Search API
   - Retrieves relevant articles and information

2. **Wikipedia Agent**
   - Encyclopedic knowledge retrieval
   - MediaWiki API integration

3. **WatsonX Crafter Agent**
   - AI-powered content synthesis
   - Report generation using IBM WatsonX foundation models

### Workflow Engine

- **Research Workflow**: Automated research pipeline
  1. Web search for current information
  2. Wikipedia knowledge retrieval
  3. AI-powered synthesis into comprehensive reports

- **Custom Workflows**: Build complex multi-step workflows with dependencies

---

## 📦 Prerequisites

- **Python**: 3.10 or higher
- **uv**: Astral's fast Python package installer ([installation](https://github.com/astral-sh/uv))
- **Docker** (optional): For containerized deployment
- **PostgreSQL** (optional): For production database
- **Redis** (optional): For distributed caching

### External Services

- **IBM Cloud Account**: For WatsonX AI access
  - API Key and Project ID required
  - Get started at [cloud.ibm.com](https://cloud.ibm.com/)

- **Google Cloud Account** (optional): For Search Agent
  - Custom Search API key required
  - Search Engine ID required
  - Configure at [console.developers.google.com](https://console.developers.google.com/)

---

## 🚀 Installation

### Quick Start with uv

```bash
# Clone the repository
git clone https://github.com/ruslanmv/Agentic-AI-on-WatsonX-with-MCP-Gateway.git
cd Agentic-AI-on-WatsonX-with-MCP-Gateway

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
make install

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### Development Installation

```bash
# Install with development dependencies
make install-dev

# Set up pre-commit hooks
make setup
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

**Required Configuration:**

```bash
# WatsonX (Required for AI synthesis)
WATSONX_API_KEY=your-watsonx-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# MCP Gateway
MCP_GATEWAY_URL=http://localhost:8080
```

**Optional Configuration:**

```bash
# Google Search (Optional)
GOOGLE_API_KEY=your-google-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id

# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/agentic_ai

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379/0
```

---

## 💻 Usage

### CLI

The CLI provides an interactive interface for the multi-agent system:

```bash
# Display help
agentic-ai --help

# View configuration
agentic-ai config

# Run demo research workflow
agentic-ai demo "Artificial Intelligence"

# Custom query
agentic-ai demo "Climate Change and Renewable Energy"

# Google search
agentic-ai search "quantum computing" --num 10

# Wikipedia lookup
agentic-ai wiki "Machine Learning" --sentences 5
```

### REST API

Start the FastAPI server:

```bash
# Using the CLI
agentic-server

# Or using make
make run

# Or with uvicorn directly
uvicorn agentic_ai.server:app --host 0.0.0.0 --port 8000
```

**API Endpoints:**

```bash
# Health check
curl http://localhost:8000/health

# List agents
curl http://localhost:8000/agents

# Execute single agent
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "wikipedia-agent",
    "task": "Artificial Intelligence",
    "context": {"sentences": 5}
  }'

# Research workflow
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Quantum Computing",
    "num_search_results": 5,
    "wiki_sentences": 5,
    "report_max_tokens": 1500
  }'
```

**Interactive API Documentation:**

Visit `http://localhost:8000/docs` for Swagger UI documentation.

### Python API

Use the agents programmatically:

```python
import asyncio
from agentic_ai.agents import WikipediaAgent, WatsonXCrafterAgent
from agentic_ai.orchestrator import AgentCoordinator, WorkflowEngine

async def main():
    # Initialize coordinator
    coordinator = AgentCoordinator()

    # Register agents
    coordinator.register_agent(WikipediaAgent())
    coordinator.register_agent(WatsonXCrafterAgent())

    # Initialize all agents
    await coordinator.initialize_all()

    # Execute single agent
    result = await coordinator.execute_agent(
        "wikipedia-agent",
        "Machine Learning"
    )
    print(result)

    # Execute research workflow
    workflow = WorkflowEngine(coordinator)
    report = await workflow.execute_research_workflow(
        query="Artificial Intelligence",
        num_search_results=5,
        wiki_sentences=5,
        report_max_tokens=1500
    )

    print(report["final_report"])

    # Cleanup
    await coordinator.cleanup_all()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🤖 Agents

### BaseAgent

All agents inherit from `BaseAgent`, providing:

- Async context manager support
- Lifecycle management (initialize, execute, cleanup)
- Error handling and validation
- Settings integration

### Creating Custom Agents

```python
from agentic_ai.agents.base import BaseAgent
from typing import Any, Optional

class CustomAgent(BaseAgent):
    async def initialize(self) -> None:
        """Initialize resources."""
        # Setup connections, load models, etc.
        self._initialized = True

    async def execute(
        self,
        task: str,
        context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Execute the agent's task."""
        self._validate_initialized()

        # Your agent logic here
        result = {"status": "success", "data": "..."}

        return result

    async def cleanup(self) -> None:
        """Clean up resources."""
        await super().cleanup()
```

---

## 🛠️ Development

### Makefile Commands

```bash
# Display all available commands
make help

# Installation
make install          # Install production dependencies
make install-dev      # Install with dev dependencies
make setup            # Complete dev environment setup

# Code Quality
make lint             # Run linting checks
make format           # Format code with black & isort
make type-check       # Run mypy type checking
make check-all        # Run all quality checks

# Testing
make test             # Run tests
make test-cov         # Run tests with coverage report
make test-watch       # Run tests in watch mode

# Cleanup
make clean            # Remove build artifacts
make clean-all        # Remove everything including venv

# Docker
make docker-build     # Build Docker image
make docker-up        # Start all services
make docker-down      # Stop all services

# Database
make db-upgrade       # Run migrations
make db-downgrade     # Rollback migration
```

### Code Quality Standards

This project enforces strict code quality:

- **Black**: Code formatting (100 char line length)
- **isort**: Import sorting
- **Ruff**: Fast Python linting
- **mypy**: Static type checking
- **pytest**: Comprehensive testing

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
uv run pytest tests/test_agents.py -v

# Run specific test
uv run pytest tests/test_agents.py::test_base_agent_initialization -v
```

**Coverage Report:**

Coverage reports are generated in `htmlcov/index.html`.

---

## 🚢 Deployment

### Docker Compose (Recommended)

```bash
# Set environment variables
export WATSONX_API_KEY=your-key
export WATSONX_PROJECT_ID=your-project
export POSTGRES_PASSWORD=secure-password

# Start all services
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

**Services:**

- **agentic-ai**: Main application (port 8000)
- **mcp-gateway**: MCP Context Forge Gateway (port 8080)
- **postgres**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)

### Kubernetes/Helm

For production Kubernetes deployment, refer to the deployment guide.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks (`make check-all test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

```
Copyright 2025 Ruslan Magana

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 🙏 Acknowledgments

- **IBM** for the MCP Context Forge Gateway and WatsonX AI platform
- **Anthropic** for the Model Context Protocol specification
- **Astral** for the uv package manager

---

## 📞 Contact

**Ruslan Magana**

- Website: [ruslanmv.com](https://ruslanmv.com)
- GitHub: [@ruslanmv](https://github.com/ruslanmv)

---

## 📚 Additional Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [IBM MCP Context Forge](https://github.com/IBM/mcp-context-forge)
- [IBM WatsonX Documentation](https://www.ibm.com/watsonx)
- [Original Developer Guide](README.original.md)

---

**Built with ❤️ by [Ruslan Magana](https://ruslanmv.com)**
