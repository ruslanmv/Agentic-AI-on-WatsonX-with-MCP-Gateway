
#  Mastering the Model Context Protocol with the MCP Gateway
## A Developer's Guide to Agentic AI

Welcome to the next frontier of AI development. In an era where Large Language Models (LLMs) have demonstrated incredible capabilities, the true challenge lies in moving beyond simple chat interfaces to build robust, autonomous systems that can solve complex, real-world problems. This is the domain of Agentic AI.

This guide provides a comprehensive overview of the Model Context Protocol (MCP), explaining how it addresses the inherent limitations of LLMs and serves as a foundational layer for creating powerful, interoperable AI Agents. We will explore a sophisticated multi-agent use case and walk through a detailed, hands-on lab to deploy the MCP Gateway—an open-source project from IBM that brings essential order, security, and scalability to the agentic AI ecosystem.

### 1. The Challenge: Overcoming the Limitations of Large Language Models

Large Language Models (LLMs) are powerful, but they are fundamentally isolated and stateless. They have core limitations that prevent them from acting effectively on their own.

**Core LLM Limitations**

  * **No Direct Access to External Systems**: An LLM cannot, by itself, access live data like weather reports, stock prices, database updates, test results, or files in your Box or Sharepoint. 
  * **No Memory Between Sessions**: Chats and interactions reset every time.  There is no native continuity or learning from past conversations, forcing users to repeat context endlessly. 
  * **Restricted Context Window**: They struggle with long documents or entire codebases because of their limited context memory. 
  * **Stateless Execution**: LLMs lack built-in flow control for managing complex, multi-step tasks that require a sequence of logical operations. 

To overcome these issues and unlock their true potential, we use **AI Agents** and **Tools**.

### 2. The Solution: AI Agents and Tools

#### What is an AI Agent?

An AI Agent is a goal-oriented, autonomous system that plans and executes multi-step tasks .  It uses an LLM as its reasoning engine to decide what to do next (a process called planning) .  These agents are powered by frameworks or orchestrators like LangChain, LangGraph, AutoGen, or watsonx Orchestrate, which execute actions by calling external APIs and Tools . 

The agent operates in a continuous, powerful loop: **Thought → Action → Observation → Repeat** until the goal is achieved. 

#### How Do Tools Empower Agents?

Tools are what allow an agent to take meaningful action in the world. They bridge the gap between the LLM's digital thoughts and real-world outcomes. Tools enable agents to:

  * Retrieve external, real-time information from sources like Google, Wikipedia, or internal corporate databases. 
  * Generate artifacts such as images, diagrams, Word documents, and Excel files. 
  * Interact with any external API and system, from project management software to cloud infrastructure controls. 

The LLM acts as the brain that turns "thought" into action. It selects the right tool for a task based on the current context and fills in the necessary parameters.  Each tool is defined by three key things: 

1.  **Name**: e.g., `Google Search` 
2.  **Description**: e.g., "Use this tool to search the internet." 
3.  **Input Schema**: e.g., `{"query": "IBM News"}` 

### 3. The Interoperability Problem: A Fragmented Tool Ecosystem

While the agent-and-tool model is powerful, its rapid, decentralized development has led to significant "growing pains" and challenges. 

  * **Fragmented Ecosystem**: Most tools are tightly coupled to specific frameworks (like LangChain or Autogen), making them difficult and costly to reuse across different platforms. 
  * **Lack of Standardization**: Each tool may have a different schema, naming convention, or prompting format, leading to immense complexity and inconsistency for developers. 
  * **Local-First Execution**: Tools often run in the same application as the agent, not as independent, reusable services, which severely limits scalability and accessibility. 
  * **No Shared Discovery**: There is no central registry or standardized way to find, share, or reuse tools across teams or even entire organizations. 

The result is high friction, redundant code, and poor interoperability.  This is the exact gap that the **Model Context Protocol (MCP)** was designed to fill. 

### 4. The Standard: Model Context Protocol (MCP)

Think of MCP as the **“USB-C for AI tools”**—a universal standard that ensures plug-and-play compatibility. 

MCP is an open protocol designed to standardize how AI agents call tools.  It provides a consistent, predictable interface for agents and applications to discover, invoke, and interact with tools, prompts, and other contextual resources.  Its adoption has been widespread and rapid, with major players like IBM, Microsoft, Google, and OpenAI embracing it. 

MCP defines a simple but powerful architecture:

  * **MCP Hosts**: AI applications, IDEs, or agentic frameworks that consume tools (e.g., LangChain, watsonx Orchestrate). 
  * **MCP Servers**: Lightweight programs that expose specific capabilities (Tools) through the standardized protocol. 
  * **MCP Clients**: Protocol clients within the Host that maintain connections to the Servers. 

This standard allows a tool to be developed once and used by any compliant agent, anywhere.  It replaces fragmented, one-off integrations with a single, governable protocol. 

### 5. The "Last Mile" Problem & The MCP Gateway

While MCP provides a standard, the ecosystem is still maturing and has evolved unevenly.  This has led to new, practical integration challenges:

  * **Inconsistent Security**: Some servers use JWT for authentication, others use OAuth2, and many use nothing at all. 
  * **Transport Variations**: Many servers still use older transports like stdio or SSE instead of the newer, more robust, streamable HTTP. 
  * **Integration Complexity**: Tools are scattered across many different servers, each with its own configuration, retry logic, and monitoring gaps. 
  * **Legacy Systems**: Existing enterprise REST APIs must be completely rewritten to become MCP-compliant, a non-starter for many organizations. 

To solve these "last-mile" integration problems, IBM Consulting developed and open-sourced the **MCP Gateway**.  The Gateway acts as a smart, unified proxy between AI agents and the various tool servers, solving critical integration pain points. 

### 6. MCP Gateway in Action: A Multi-Agent Research Assistant

To understand the power of the gateway, let's consider a more sophisticated, multi-agent workflow.

#### Use Case: The Multi-Agent Research Assistant

An AI orchestrator agent is tasked with a complex request: "Create a detailed report on the latest advancements in AI hardware, including key players and market trends." To do this, it needs to gather, process, and synthesize information from multiple sources.

  * **The Agents & Their Roles**:

    1.  **`google-search-agent`**: A specialized "worker" agent whose only job is to perform web searches and retrieve up-to-date articles and links. 
    2.  **`wikipedia-agent`**: Another "worker" agent designed to fetch foundational, encyclopedic knowledge about topics, companies, and technologies. 
    3.  **`watsonx-crafter-agent`**: A powerful "synthesis" agent. Its tool is a connection to a `watsonx.ai` foundation model. Its role is not to fetch data, but to receive structured data from other agents and use the reasoning power of `watsonx.ai` to craft a final, coherent report.

  * **The Challenge**: The orchestrator needs to manage three separate agents, handle their individual outputs, and sequence the workflow correctly. The tool agents might have different security requirements, and the final call to the powerful `watsonx.ai` model needs to be governed and logged.

  * **The MCP Gateway Solution**: The gateway acts as the central nervous system for this operation. 

    1.  The orchestrator sends all tool requests to the single, unified endpoint of the MCP Gateway.
    2.  The gateway securely routes requests to the appropriate agent: search queries go to the `google-search-agent`, topic lookups go to the `wikipedia-agent`. It handles the distinct authentication and protocols for each. 
    3.  Once the worker agents return their raw data, the orchestrator passes this data as context in a final tool call to the gateway, destined for the `watsonx-crafter-agent`.
    4.  The gateway forwards this rich context to the `watsonx-crafter-agent`, which uses `watsonx.ai` to generate the final, high-quality report. The gateway provides full observability and governance over this entire workflow. 

### 7. MCP Gateway Architecture Deep Dive

The architecture of the MCP Gateway is designed for this kind of modularity and orchestration. The **MCP Gateway Core** is the central hub that connects the UI and authentication layers with various backend services, caching, and persistence layers.

```mermaid
graph TD
    subgraph UI_and_Auth
        A[Admin UI]
        B[Auth - JWT and Basic]
    end

    subgraph Core
        C[MCP Gateway Core]
    end

    subgraph Caching
        D[Cache - Redis or Memory]
    end

    subgraph Services
        E[Tool Service]
        F[Resource Service]
        G[Prompt Service]
        H[Server Service]
    end

    subgraph Persistence
        I[Database - SQLAlchemy]
    end

    subgraph Gateway_Core_Features
        direction LR
        J[Protocol - Int Ping Completion]
        K[Federation Manager]
    end
    
    subgraph Transports
        L[Transports - HTTP WS SSE Stdio]
    end

    A --> C
    B --> C

    C --> D
    C --> E
    C --> F
    C --> G
    C --> H
    C --> J
    C --> K
    C --> L

    E --> I
    F --> I
    G --> I
    H --> I
```
### 8. Hands-On Lab: Building the Multi-Agent Research Assistant



This section provides a conceptual overview of the steps to get the Multi-Agent Research Assistant running.

#### 1. Prerequisites

  * Docker & Docker Compose (for containerized deployment), or
  * Python 3.9+, Go 1.18+, and PostgreSQL (for local development)
  * Git

#### 2. Clone & Configure

First, you'll clone the repository and create your local environment configuration files from the provided examples.

```bash
# Clone the repository
git clone https://github.com/IBM/mcp-context-forge.git
cd mcp-context-forge
git checkout v0.2.0 

# Copy example environment files
cp .env.example .env
cp .env.ce.example .env.ce
```
Now, edit the `.env` file to add your database connection string and configure the gateway host.

```bash
# --- WatsonX Credentials ---
# Required only if you implement the watsonx-crafter-agent's logic.
# Obtain these credentials from your IBM Cloud IAM.
WATSONX_API_KEY=YOUR_WATSONX_KEY
WATSONX_URL=https://us-south.api.watsonx.ai
PROJECT_ID=YOUR_PROJECT_ID



# --- PostgreSQL Connection Settings ---
# These variables are used by the 'db' service in docker-compose.yml
# and by the gateway to connect to the database.
POSTGRES_USER=postgres # Default database user
POSTGRES_PASSWORD=mysecretpassword # Default database password (change for production)
POSTGRES_DB=mcp # Database name used by the Gateway

# --- Gateway Network Settings ---
GATEWAY_HOST=0.0.0.0 # Binds to all available network interfaces on the host.
GATEWAY_PORT=8000 # The external port the gateway will be accessible on.

```




#### 3. Start the Gateway Core

Using Docker Compose is the recommended method. A single command will start the PostgreSQL database and the MCP Gateway service. You can also run the gateway directly with Python, but Docker Compose provides an isolated, reproducible environment.

---

**A) Using Docker Compose**

1. **Ensure your `.env` file** lives alongside `docker-compose.yml` and contains at least the necessary variables (e.g. `POSTGRES_PASSWORD`, `JWT_SECRET_KEY`, etc.). Compose will automatically interpolate `${…}` references and, if you’ve added `env_file: - .env` under each service, also inject every variable into the container.

2. **Verify the Compose V2 plugin** is available:

   ```bash
   docker compose version
   ```

3. **Bring up the services** (service names are `postgres`, `redis`, and `gateway`):

   ```bash
   docker compose up -d postgres redis gateway
   ```

4. **Wait for the gateway to pass its healthcheck.** The Compose file defines a healthcheck for the `gateway` service on port 4444. You can monitor all service statuses:

   ```bash
   docker compose ps
   ```

   Look for something like:

   ```
   Name                           Service   State                     Ports
   ---------------------------------------------------------------------------
   mcp-context-forge-postgres-1   postgres  Up (healthy)              5432/tcp
   mcp-context-forge-redis-1      redis     Up                        0.0.0.0:6379->6379/tcp
   mcp-context-forge-gateway-1    gateway   Up (healthy)              0.0.0.0:4444->4444/tcp
   ```

5. **Verify the health endpoint** once the gateway is `Up (healthy)`:

   ```bash
   curl http://localhost:4444/health
   # → {"status":"ok"}
   ```

---

**B) (Alternate) Run Locally with Python**

If you prefer not to use Docker:

1. **Install dependencies** and create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run database migrations**:

   ```bash
   alembic upgrade head
   ```

3. **Start the gateway** on port 4444:

   ```bash
   HOST=0.0.0.0 PORT=4444 ./run-gunicorn.sh
   ```

4. **Verify health**:

   ```bash
   curl http://localhost:4444/health
   # → {"status":"ok"}
   ```

With either approach, your MCP Gateway Core should now be running and ready to accept agent registrations and client requests.



#### 4. Create & Launch the Researcher Agents

You will use the sample Go-based agent in the repository as a template to create three distinct agents: `google-search-agent`, `wikipedia-agent`, and `watsonx-crafter-agent`. After building their Docker images, you will run them as containers on the same Docker network as the gateway.

**A) Copy & Customize the Agent Code**

```bash
# Create the Google Search Agent
cp -r mcp-servers/go/fast-time-server mcp-servers/go/google-search-agent

# Create the Wikipedia Agent
cp -r mcp-servers/go/fast-time-server mcp-servers/go/wikipedia-agent

# Create the watsonx Crafter Agent
cp -r mcp-servers/go/fast-time-server mcp-servers/go/watsonx-crafter-agent
```

For each new agent, you would typically rename the module in its `go.mod` file and update the logic in `main.go` to expose the actual tool capabilities (e.g., calling the Google Search API, Wikipedia API, or the watsonx.ai API).



# Build Google Search Agent


# Build Wikipedia Agent



# Build watsonx Crafter Agent


**B) Build Docker Images for the Agents**

```bash
# Build Google Search Agent
cd mcp-servers/go/google-search-agent
docker build -t google-search-agent:local .
cd ../../..

# Build Wikipedia Agent
cd mcp-servers/go/wikipedia-agent
docker build -t wikipedia-agent:local .
cd ../../..

# Build watsonx Crafter Agent
cd mcp-servers/go/watsonx-crafter-agent
docker build -t watsonx-crafter-agent:local .
cd ../../..
```

**C) Run the Agents as Containers**

```bash
# Run google-search-agent container
docker run -d --name google-search-agent \
  --network mcp-context-forge_default \
  --env GATEWAY_URL=http://mcpgateway:8000 \
  google-search-agent:local

# Run wikipedia-agent container
docker run -d --name wikipedia-agent \
  --network mcp-context-forge_default \
  --env GATEWAY_URL=http://mcpgateway:8000 \
  wikipedia-agent:local

# Run watsonx-crafter-agent container
docker run -d --name watsonx-crafter-agent \
  --network mcp-context-forge_default \
  --env GATEWAY_URL=http://mcpgateway:8000 \
  watsonx-crafter-agent:local
```


#### 5. Register Agents with the Gateway

With the agents running, the final step is to tell the gateway about them. You can do this easily via the Admin UI or by sending a `cURL` request to the gateway's REST API for each agent.


**Using the REST API (curl)**

```bash
# Register google-search-agent
curl -X POST http://localhost:8000/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "google-search-agent",
    "url":  "http://google-search-agent:8080"
}'

# Register wikipedia-agent
curl -X POST http://localhost:8000/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "wikipedia-agent",
    "url":  "http://wikipedia-agent:8080"
}'

# Register watsonx-crafter-agent
curl -X POST http://localhost:8000/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "watsonx-crafter-agent",
    "url":  "http://watsonx-crafter-agent:8080"
}'
```

**Using the Admin UI**

1.  Open `http://localhost:8000/admin` in your browser.
2.  Navigate to “Servers” → “Add Server”.
3.  Fill in the Name (e.g., `google-search-agent`) and URL (`http://google-search-agent:8080`), then save. Repeat for the `wikipedia-agent` and `watsonx-crafter-agent`.

#### 6. Verification

A simple API call to the gateway's `/servers` endpoint will list all registered agents, confirming your multi-agent system is online and ready for action.


List all registered servers to confirm success:

```bash
curl http://localhost:8000/api/v1/servers
```

You should see a JSON response listing `google-search-agent`, `wikipedia-agent`, and `watsonx-crafter-agent`. At this point, your core Gateway is running and ready to federate requests across all three agents for your Multi-Agent Research Assistant\!


#### 4. One-Command Demo Script

Create a file named `demo.sh` at the repository root. This script automates the entire setup process.

```bash
#!/usr/bin/env bash
# This script provides a one-command way to start the entire demo environment.
set -eux

echo "--- 1. Starting Database and MCP Gateway... ---"
docker-compose up -d db mcpgateway

# Wait for gateway to be healthy
until [ "$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health)" = "200" ]; do
    echo "Waiting for gateway to be healthy..."
    sleep 2
done
echo "Gateway is up and running."

echo "--- 2. Building Agent Docker Images... ---"
docker build -t google-search-agent:demo ./mcp-servers/go/google-search-agent
docker build -t wikipedia-agent:demo ./mcp-servers/go/wikipedia-agent
docker build -t watsonx-crafter-agent:demo ./mcp-servers/go/watsonx-crafter-agent

echo "--- 3. Running Agent Containers... ---"
docker run -d --rm --name google-search-agent --network mcp-context-forge_default \
  -e GATEWAY_URL=http://mcpgateway:8000 google-search-agent:demo
docker run -d --rm --name wikipedia-agent --network mcp-context-forge_default \
  -e GATEWAY_URL=http://mcpgateway:8000 wikipedia-agent:demo
docker run -d --rm --name watsonx-crafter-agent --network mcp-context-forge_default \
  -e GATEWAY_URL=http://mcpgateway:8000 watsonx-crafter-agent:demo

echo "--- 4. Registering Agents with the Gateway... ---"
for AGENT in google-search-agent wikipedia-agent watsonx-crafter-agent; do
  echo "Registering $AGENT..."
  curl -s -X POST http://localhost:8000/servers \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$AGENT\",\"url\":\"http://$AGENT:8080\"}"
done

echo "--- 5. Smoke Test: Verifying Registered Servers... ---"
curl -s http://localhost:8000/api/v1/servers | jq .

echo "--- Demo Setup Complete! ---"
```

Make it executable:

```bash
chmod +x demo.sh
```

#### 5. Final `docker-compose.yml` & Helm Values

The `docker-compose.yml` file at the root of the repository orchestrates the local services.

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

  mcpgateway:
    build:
      context: .
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "${GATEWAY_PORT}:8000"

volumes:
  pgdata:
```

For Kubernetes deployments, you can use the provided Helm chart with these value overrides.

```yaml
# charts/context-forge/values.yaml (example overrides)
replicaCount: 2

image:
  repository: ibmcom/mcp-context-forge
  tag: v1.3.0 # Use a specific release tag

env:
  GATEWAY_PORT: "8000"
  DATABASE_URL: "postgresql://user:pass@postgres-service:5432/mcp"
  JWT_SECRET: "your-production-jwt-secret-from-k8s-secrets"
```

```bash
# Helm Install Command
helm repo add ibm-mcp https://ibm.github.io/mcp-context-forge/
helm upgrade --install mcp-gateway ibm-mcp/context-forge \
  -f my-values.yaml
```

#### 6. Copy-Paste Code Snippets with File Paths

To create the agent logic, you would modify the `main.go` file inside each agent's directory.

```go
// File: mcp-servers/go/google-search-agent/main.go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func searchHandler(w http.ResponseWriter, r *http.Request) {
	query, _ := io.ReadAll(r.Body)
	// In a real implementation, you would call the Google Search API here.
	fmt.Fprintf(w, "Search results for query: %s", string(query))
}

func main() {
	http.HandleFunc("/search", searchHandler)
	http.ListenAndServe(":8080", nil)
}
```

You would apply similar logic to the `wikipedia-agent` (calling a Wikipedia library) and the `watsonx-crafter-agent` (calling the WatsonX API).

#### 7. Automated Test Suite

The repository includes tests for the Python gateway and Go agents.

```python
# File: tests/smoketest.py (conceptual)
import requests
import os

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")

def test_gateway_health():
    response = requests.get(f"{GATEWAY_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_registered_servers_exist():
    response = requests.get(f"{GATEWAY_URL}/api/v1/servers")
    assert response.status_code == 200
    server_names = [s['name'] for s in response.json()]
    assert "google-search-agent" in server_names
    assert "wikipedia-agent" in server_names
```

```bash
# Run all Python tests
pytest
```

#### 8. Architecture Diagram & Network Callouts

```mermaid
graph TD
    subgraph User Interaction
        User[User/Orchestrator]
    end

    subgraph "Docker Network: mcp-context-forge_default"
        subgraph "MCP Gateway Container (mcpgateway)"
            GW[Gateway Service on :8000]
        end
        subgraph "Postgres Container (db)"
            DB[Postgres on :5432]
        end
        subgraph "Agent Containers"
            GSA[google-search-agent on :8080]
            WA[wikipedia-agent on :8080]
            WCA[watsonx-crafter-agent on :8080]
        end
    end

    User -- "HTTP API Call (localhost:8000)" --> GW
    GW -- "TCP/SQL (db:5432)" --> DB
    GW -- "HTTP (google-search-agent:8080)" --> GSA
    GW -- "HTTP (wikipedia-agent:8080)" --> WA
    GW -- "HTTP (watsonx-crafter-agent:8080)" --> WCA
```

#### 9. Logging & Monitoring Examples

```bash
# View live logs for the gateway
docker-compose logs -f mcpgateway

# View logs for a specific agent
docker logs -f google-search-agent

# Key log lines to watch for in gateway logs:
#   INFO  alembic.runtime.migration: Running upgrade ... -> ...
#   INFO  uvicorn.error: Uvicorn running on http://0.0.0.0:8000
#   INFO:     127.0.0.1:54321 - "POST /servers HTTP/1.1" 200 OK
```


#### 11. Security Walkthrough

To enable Basic Auth, uncomment the relevant security dependency in `mcpgateway/main.py` and protect endpoints as shown in the file. Your `.env` file must contain `BASIC_AUTH_USERNAME` and `BASIC_AUTH_PASSWORD`.

To enable TLS for the gateway, first generate a self-signed certificate:

```bash
# Generate a key and certificate valid for 365 days
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 \
  -nodes -subj "/CN=localhost"
```

Then, mount these files and update the command in your `docker-compose.yml`:

```yaml
# In docker-compose.yml
services:
  mcpgateway:
    # ...
    volumes:
      - ./cert.pem:/app/cert.pem
      - ./key.pem:/app/key.pem
    command: >
      sh -c "alembic upgrade head &&
             gunicorn --worker-class uvicorn.workers.UvicornWorker
                      --config ./gunicorn.conf.py mcpgateway.main:app
                      --keyfile /app/key.pem --certfile /app/cert.pem"
```

#### 12. Performance & Scaling Guides

The `gunicorn.conf.py` file controls the number of gateway workers. A good starting point is `(2 x CPU_CORES) + 1`.

```python
# File: gunicorn.conf.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 60
```

To scale services with Docker Compose, use the `--scale` flag:

```bash
docker-compose up -d --scale mcpgateway=3
```

In Kubernetes, simply increase the `replicaCount` in your Helm `values.yaml`.

#### 13. CI/CD Pipeline Config

The repository includes a sample GitHub Actions workflow in `.github/workflows/ci.yml`.

```yaml
# File: .github/workflows/ci.yml (excerpt)
name: CI

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install Python dependencies
        run: pip install -r requirements.txt
      - name: Lint Python Code
        run: make lint
      - name: Run Python Tests
        run: make test
      - name: Build Gateway Docker image
        run: docker build -t ibmcom/mcp-gateway:latest .
```


## Troubleshotings


### Delete container
### 1) If you brought them up with Docker Compose
From the same folder as your `docker-compose.yml`, simply run:
```bash
docker compose down
```
This will stop **and** remove all containers, networks and named volumes created by `docker compose up`.
---
### 2) Using plain Docker commands

To stop **all** running containers:

```bash
docker stop $(docker ps -q)
```

If you also want to remove them afterwards:

```bash
docker rm $(docker ps -aq)
```

* `docker ps -q` lists only running container IDs
* `docker ps -aq` lists **all** container IDs (running or stopped)

## Recreate your stack

```bash
docker compose down
docker compose up -d postgres redis gateway
```

Watch the logs:

```bash
docker compose logs -f gateway
```

You should see:

```
INFO  alembic.runtime.migration: Running upgrade -> head
INFO  uvicorn.error: Uvicorn running on http://0.0.0.0:4444
```

And `docker compose ps` eventually shows:

```
mcp-context-forge-gateway-1   Up (healthy)   0.0.0.0:4444->4444/tcp
```

Finally, confirm:

```bash
curl http://localhost:4444/health
# → {"status":"ok"}
```



## Conclusion

You’ve now seen how the Model Context Protocol (MCP) and the MCP Gateway transform isolated LLM experiments into full-blown, multi-agent AI systems—secure, auditable, and scalable. By standardizing agent-to-tool communications under one unified HTTP interface, you eliminate brittle one-offs, centralize authentication and observability, and empower teams to develop and share reusable “plug-and-play” services. 

Thank you for mastering the MCP Gateway on WatsonX—now go build something extraordinary.



