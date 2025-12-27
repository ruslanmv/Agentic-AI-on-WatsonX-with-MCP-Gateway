# Agentic AI on watsonx with MCP Gateway (ContextForge)
## Production-Ready Developer Guide

**Step-by-step documentation to become an expert user.**
**Includes end-to-end multi-agent examples with CrewAI and Langflow.**

---

**Repository:** IBM/mcp-context-forge (ContextForge MCP Gateway)
**Audience:** Developers, platform engineers, AI engineers
**Last updated:** 2025-12-27

---

## Table of Contents

1. [What you are building](#1-what-you-are-building)
2. [Core concepts](#2-core-concepts-agentic-ai-mcp-gateway)
3. [Repository tour](#3-repository-tour-how-the-codebase-is-organized)
4. [Quickstart (local dev)](#4-quickstart-local-dev)
5. [Configuration that matters in production](#5-configuration-that-matters-in-production)
6. [Understanding the Gateway API surface](#6-understanding-the-gateway-api-surface)
7. [Building and registering MCP servers](#7-building-and-registering-mcp-servers-tools)
8. [End-to-end example: Multi-agent system with CrewAI + Langflow](#8-end-to-end-example-multi-agent-system-with-crewai--langflow-via-the-gateway)
9. [Production hardening guide](#9-production-hardening-guide)
10. [Troubleshooting playbook](#10-troubleshooting-playbook)
11. [Reference links](#11-reference-links-external)

---

## 1. What you are building

You are building a production-ready **"tool fabric"** for agentic applications: a centralized MCP Gateway that federates many Model Context Protocol (MCP) servers (tools) and legacy REST/gRPC services into one governed endpoint.

Your agents (CrewAI, Langflow, LangChain, etc.) connect to the Gateway once, then discover and invoke tools consistently.

---

## 2. Core concepts (Agentic AI, MCP, Gateway)

### 2.1 Agentic AI: why chatbots aren't enough

- **LLMs are stateless** and do not have native access to your systems (databases, SaaS tools, internal APIs).
- **Agents add planning + execution loops**: Thought → Action (tool call) → Observation → Repeat.
- **Tools are the bridge** from model reasoning to real-world actions (APIs, files, DBs, workflows).

### 2.2 MCP: the "USB-C" for tools

**Model Context Protocol (MCP)** standardizes how an AI client discovers and calls tools, prompts, and resources. A single MCP tool can be reused across many frameworks, avoiding one-off integrations.

### 2.3 ContextForge MCP Gateway: the enterprise "last mile"

- **Unified registry**: tools, prompts, resources, servers, and optional A2A (agent-to-agent) endpoints.
- **Protocol bridging**: MCP over streamable HTTP/SSE/WebSocket/JSON-RPC plus REST-to-MCP and gRPC-to-MCP adapters.
- **Production controls**: auth, rate limits, retries, observability, caching, multi-tenant/RBAC features (version-dependent).
- **Optional Admin UI** for development-time management (do not expose publicly in production).

---

## 3. Repository tour (how the codebase is organized)

This project is large and includes: the FastAPI gateway, an Admin UI, Helm charts, deployment automation, agent runtimes, plugins, and extensive documentation.

### 3.1 Top-level folders you will use most

| Path | Purpose |
|------|---------|
| `mcpgateway/` | Gateway core (FastAPI app, services, transports, auth, middleware, DB models). |
| `docs/docs/` | Documentation site sources (architecture, deployment, operations, tutorials). |
| `charts/` | Helm charts for Kubernetes deployments (including stacks). |
| `deployment/` | Terraform/Ansible/Knative/K8s manifests and helpers. |
| `agent_runtimes/` | Example runtime integrations for agents (e.g., LangChain). |
| `mcp-servers/` | Example MCP servers (language-specific templates) and adapters. |
| `tests/` | Automated tests and smoke tests. |

### 3.2 Gateway request flow (mental model)

1. AI client connects to Gateway (MCP transport).
2. Gateway authenticates the client (JWT/OAuth/Basic depending on configuration).
3. Client calls: `list_tools` / `call_tool` (and `list_resources`/`prompts` if used).
4. Gateway routes the call to a registered upstream MCP server OR to a virtual tool (REST/gRPC adapter).
5. Gateway applies retries, rate limits, auditing, and logs/telemetry, then returns normalized results.

---

## 4. Quickstart (local dev)

Two recommended ways to start locally: PyPI (fastest) or Docker Compose (closest to production).

### 4.1 Option A - Run from PyPI

```bash
python -m venv .venv
source .venv/bin/activate
pip install mcp-contextforge-gateway

# Start with defaults (SQLite by default; good for dev)
mcpgateway
```

### 4.2 Option B - Run with Docker Compose (Postgres + Redis + Gateway)

Use this for realistic local environments and for most demos.

```bash
# From repository root
cp .env.example .env

# Edit .env: set secrets, DB URLs, auth mode, etc.
docker compose up -d postgres redis gateway

# Health
curl http://localhost:4444/health
```

### 4.3 Verify you can register and list servers

The gateway exposes server management APIs under the `/servers` routes.

```bash
# Create (register) an upstream MCP server
curl -X POST http://localhost:4444/servers \
  -H "Content-Type: application/json" \
  -d '{"name":"wikipedia-agent","url":"http://wikipedia-agent:8080"}'

# List servers
curl http://localhost:4444/servers
```

---

## 5. Configuration that matters in production

### 5.1 Secrets and environment variables

ContextForge is configured primarily via environment variables (often loaded from a `.env` file). For production: store secrets in a secret manager (Kubernetes Secrets, Vault, IBM Secrets Manager) and inject at runtime.

### 5.2 Production checklist

- Disable or restrict Admin UI (localhost only).
- Enable authentication for all endpoints (JWT/OAuth2) and rotate keys.
- Terminate TLS at an ingress or enable TLS on the gateway container.
- Use Postgres for persistence; use Redis for caching/federation at scale.
- Enable OpenTelemetry export to your tracing backend (Jaeger/Tempo/OTLP).
- Set conservative timeouts, retry policies, and rate limits per upstream server.
- Use RBAC/teams (if your deployed version supports it) to prevent tool leakage across tenants.

---

## 6. Understanding the Gateway API surface

The Gateway is both an **MCP server** and a **management API**. You use MCP for tool invocation from AI clients, and REST APIs for ops (register servers, manage virtual tools, prompts, resources).

### 6.1 Operational REST routes (examples)

- **Servers**: `/servers` (CRUD)
- **Tools**: `/tools` (CRUD, including virtual tools mapped to REST/gRPC)
- **Resources**: `/resources` (CRUD + subscriptions where supported)
- **Prompts**: `/prompts` (CRUD + execute)
- **Health**: `/health`

### 6.2 MCP transports (how clients connect)

- Streamable HTTP (recommended)
- SSE (fallback)
- WebSocket
- JSON-RPC over HTTP
- stdio (wrapper mode for desktop/CLI clients)

---

## 7. Building and registering MCP servers (tools)

You can integrate tools in three ways:

1. **Register an upstream MCP server** (preferred)
2. **Virtualize a legacy REST API** as MCP tools (no rewrite)
3. **Virtualize gRPC services** via reflection (where supported)

### 7.1 Pattern A - Register a real MCP server

Run the server, then register it with the Gateway.

```bash
# Example: server running at http://my-mcp-server:8080
curl -X POST http://localhost:4444/servers \
  -H "Content-Type: application/json" \
  -d '{"name":"my-tools","url":"http://my-mcp-server:8080","description":"Internal tools"}'
```

### 7.2 Pattern B - Wrap a REST API as tools (virtual server)

ContextForge can expose REST endpoints as MCP tools by defining tool metadata and a mapping (including auth headers, JSON schema, and response extraction). This is how you avoid rewriting existing enterprise APIs.

---

## 8. End-to-end example: Multi-agent system with CrewAI + Langflow (via the Gateway)

### Goal
Build a research assistant where a CrewAI "manager" delegates to tool-using agents. Tools come from multiple MCP servers and from a Langflow flow exposed as an MCP server. All tool access goes through ContextForge for governance.

### 8.1 Architecture for the demo

- **ContextForge MCP Gateway**: single MCP endpoint for the AI app.
- **Upstream MCP servers**: a search tool server and a Wikipedia tool server.
- **Langflow**: one flow exposed as an MCP server tool (e.g., summarize URLs or extract structured facts).
- **CrewAI**: orchestrates agents and calls tools through MCP.

### 8.2 Step 1 - Start the Gateway stack

```bash
# In repo root
cp .env.example .env

# Recommended: Postgres + Redis + Gateway
docker compose up -d postgres redis gateway

curl http://localhost:4444/health
```

### 8.3 Step 2 - Run example MCP tool servers

Use any MCP servers you like (Go/Python/Node). For a demo, start simple servers exposing tools like:
- `web_search(query)`
- `wikipedia_summary(topic)`

Then run them on the same Docker network as the gateway.

```bash
# Example (conceptual): run tool servers on the compose network
docker run -d --name wikipedia-agent --network mcp-context-forge_default my-wikipedia-mcp:latest
docker run -d --name search-agent    --network mcp-context-forge_default my-search-mcp:latest
```

### 8.4 Step 3 - Register those servers in ContextForge

```bash
curl -X POST http://localhost:4444/servers -H "Content-Type: application/json" \
  -d '{"name":"wikipedia-agent","url":"http://wikipedia-agent:8080"}'

curl -X POST http://localhost:4444/servers -H "Content-Type: application/json" \
  -d '{"name":"search-agent","url":"http://search-agent:8080"}'

curl http://localhost:4444/servers
```

### 8.5 Step 4 - Run Langflow and expose a flow as an MCP server

Langflow can run as an MCP server and expose flows as tools, using streamable HTTP (and SSE fallback). Create a flow (e.g., "Summarize URLs and extract citations"), then enable its MCP server mode.

```bash
# Example: run Langflow (adjust to your environment)
pip install langflow
langflow run --host 0.0.0.0 --port 7860

# In the Langflow UI:
# - Build and save a Flow
# - Enable MCP Server for the Flow (docs.langflow.org -> MCP server)
```

Register Langflow's MCP endpoint in the Gateway:

```bash
curl -X POST http://localhost:4444/servers -H "Content-Type: application/json" \
  -d '{"name":"langflow-tools","url":"http://langflow:7860/mcp"}'
```

### 8.6 Step 5 - CrewAI project: connect to the Gateway via MCP

CrewAI supports MCP servers as tools. The simplest approach is to point CrewAI at the Gateway's MCP endpoint, so your Crew automatically has access to the federated toolset.

```bash
# Create a new project
pip install crewai crewai-tools

crewai create crew mcp_research_crew
cd mcp_research_crew
```

Example CrewAI code (Python) using MCP tools via the Gateway:

```python
# file: src/mcp_research_crew/crew.py
from crewai import Agent, Task, Crew, Process

# CrewAI MCP support uses the 'mcps' field on agents (see CrewAI MCP docs).
# Point this to the ContextForge MCP endpoint (streamable HTTP recommended).
GATEWAY_MCP_URL = "http://localhost:4444/mcp"

researcher = Agent(
    role="Researcher",
    goal="Find recent, high-quality sources about AI hardware advances and summarize them.",
    backstory="You are an expert research analyst.",
    mcps=[{"name": "contextforge", "url": GATEWAY_MCP_URL}],
    verbose=True,
)

synthesizer = Agent(
    role="Synthesizer",
    goal="Create a structured report with citations and key trends.",
    backstory="You write crisp technical briefs for executives.",
    mcps=[{"name": "contextforge", "url": GATEWAY_MCP_URL}],
    verbose=True,
)

t1 = Task(
    description="Use search tools to find 5-8 recent articles about AI hardware (chips, accelerators, interconnects).",
    expected_output="A bullet list of URLs and 1-2 sentence notes for each.",
    agent=researcher,
)

t2 = Task(
    description="Use Wikipedia and Langflow tools to extract background and produce a final report with sections: key players, tech trends, market signals.",
    expected_output="A 2-4 page report with citations.",
    agent=synthesizer,
)

crew = Crew(
    agents=[researcher, synthesizer],
    tasks=[t1, t2],
    process=Process.sequential,
)

if __name__ == "__main__":
    print(crew.kickoff())
```

### 8.7 Step 6 - Use Langflow as an MCP client (optional)

Langflow can also act as an MCP client. You can connect Langflow to the Gateway and use MCP Tools components inside flows to call the same federated tools.

```bash
# In Langflow UI:
# - Add an MCP Tools component
# - Configure MCP server URL to the Gateway MCP endpoint
# - Use tools inside a flow, then re-expose that flow as an MCP server
```

---

## 9. Production hardening guide

### 9.1 Networking and TLS

- Run the gateway behind an ingress (NGINX/Traefik/Envoy) with TLS and WAF rules.
- If using self-signed TLS for dev, mount certs and configure the gateway's server command accordingly.
- Lock down CORS to known frontends.

### 9.2 Authentication and authorization

- Prefer OAuth2/OIDC for human users and JWT for service-to-service automation.
- Rotate JWT signing keys and use short token lifetimes.
- Use RBAC/teams for tool visibility if your deployed version includes these features.
- Never rely on the Admin UI for production access control; treat it as a dev-only tool.

### 9.3 Reliability controls

- Configure retries with backoff for flaky upstream tools; disable retries for non-idempotent operations.
- Set timeouts per upstream server based on expected latency.
- Add circuit breakers via gateway policies or upstream proxies for "blast radius" control.

### 9.4 Observability

- Enable OpenTelemetry export and propagate correlation IDs.
- Capture tool call metrics: latency, error rate, retries, upstream service health.
- Use structured logging and central log aggregation (ELK/Loki).

---

## 10. Troubleshooting playbook

- **Gateway won't start**: check DB/Redis readiness, migrations, and env variables.
- **Can't register servers**: verify auth, confirm server URL is reachable from gateway network, inspect logs.
- **Tools don't appear in client**: ensure server is healthy and MCP discovery endpoints respond.
- **Streaming issues**: try streamable HTTP first; SSE as fallback; check proxy buffering settings.

---

## 11. Reference links (external)

Use these official references for the most up-to-date behavior and integration details:

- [IBM ContextForge MCP Gateway (GitHub)](https://github.com/IBM/mcp-context-forge)
- [ContextForge documentation site](https://ibm.github.io/mcp-context-forge/)
- [MCP specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18)
- [CrewAI MCP docs](https://docs.crewai.com/en/mcp/overview)
- [Langflow MCP server docs](https://docs.langflow.org/mcp-server)
- [Langflow MCP client docs](https://docs.langflow.org/mcp-client)
- [Langflow blog (MCP integration)](https://www.langflow.org/blog/introducing-mcp-integration-in-langflow)

---

**Copyright 2025 Ruslan Magana**
**Licensed under Apache License 2.0**
