# Complete Demo Guide: MCP Gateway with CrewAI and Langflow

This guide provides step-by-step instructions to run a complete demo showcasing the integration of MCP Context Forge Gateway, CrewAI, and Langflow.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Phase](#setup-phase)
4. [Demo 1: Simple Research Assistant](#demo-1-simple-research-assistant)
5. [Demo 2: Multi-Agent Research System](#demo-2-multi-agent-research-system)
6. [Demo 3: Customer Support Automation](#demo-3-customer-support-automation)
7. [Troubleshooting](#troubleshooting)

---

## Overview

**What you'll build:**
- A federated MCP Gateway connecting multiple tool servers
- Langflow workflows exposed as MCP tools
- CrewAI agents using all tools through the gateway

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│               CrewAI Multi-Agent System                  │
│           (Research Crew, Support Crew, etc.)            │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
┌────────────────────▼────────────────────────────────────┐
│          ContextForge MCP Gateway (Port 4444)            │
│              (Tool Federation Layer)                     │
└──┬──────────┬──────────┬──────────┬──────────┬──────────┘
   │          │          │          │          │
┌──▼───┐  ┌──▼───┐  ┌──▼───┐  ┌──▼───┐  ┌──▼───────┐
│Search│  │ Wiki │  │ DB   │  │ API  │  │ Langflow │
│Tools │  │Tools │  │Tools │  │Tools │  │ Flows    │
└──────┘  └──────┘  └──────┘  └──────┘  └──────────┘
```

---

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Docker**: Version 20.10 or higher
- **Python**: 3.10 or higher
- **Storage**: 10GB free space

### Required Software
```bash
# Check installations
docker --version          # Should be 20.10+
docker-compose --version  # Should be 1.29+
python3 --version        # Should be 3.10+
```

### Required API Keys (for full demo)
- **IBM WatsonX** (for AI models)
- **Google Custom Search** (optional, for web search)

---

## Setup Phase

### Step 1: Clone and Setup Repository

```bash
# Clone repository
git clone https://github.com/ruslanmv/Agentic-AI-on-WatsonX-with-MCP-Gateway.git
cd Agentic-AI-on-WatsonX-with-MCP-Gateway

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required environment variables:**
```bash
# WatsonX Configuration
WATSONX_API_KEY=your-api-key-here
WATSONX_PROJECT_ID=your-project-id-here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# MCP Gateway
MCP_GATEWAY_URL=http://localhost:4444

# Optional: Google Search
GOOGLE_API_KEY=your-google-api-key
GOOGLE_SEARCH_ENGINE_ID=your-search-engine-id
```

### Step 2: Start Infrastructure Services

```bash
# Start Postgres, Redis, and MCP Gateway
docker-compose up -d postgres redis gateway

# Verify services are running
docker-compose ps

# Check gateway health
curl http://localhost:4444/health
```

**Expected output:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "connected"
  }
}
```

### Step 3: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install CrewAI and Langflow
pip install crewai crewai-tools langflow
```

### Step 4: Setup MCP Tool Servers

**Option A: Use existing agents (simple)**

```bash
# The repository includes Wikipedia and Google Search agents
# They'll connect automatically to MCP Gateway

# Verify agents are running
curl http://localhost:4444/servers
```

**Option B: Add custom MCP servers (advanced)**

Create a simple MCP server for demonstration:

```python
# simple_mcp_server.py
from fastapi import FastAPI
from typing import Dict, Any

app = FastAPI()

@app.get("/mcp/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "echo",
                "description": "Echo back the input",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"}
                    },
                    "required": ["message"]
                }
            }
        ]
    }

@app.post("/mcp/call_tool")
def call_tool(request: Dict[str, Any]):
    if request["tool"] == "echo":
        return {"result": f"Echo: {request['arguments']['message']}"}

# Run: uvicorn simple_mcp_server:app --port 8081
```

Register with gateway:
```bash
curl -X POST http://localhost:4444/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "echo-server",
    "url": "http://localhost:8081",
    "description": "Simple echo server for testing"
  }'
```

### Step 5: Setup and Configure Langflow

```bash
# Install and run Langflow
pip install langflow
langflow run --host 0.0.0.0 --port 7860 &

# Wait for Langflow to start
sleep 10

# Access Langflow UI
echo "Langflow UI: http://localhost:7860"
```

**Create a sample flow in Langflow UI:**

1. Open http://localhost:7860
2. Create new flow: "Text Summarizer"
3. Add components:
   - Text Input → LLM (with summarization prompt) → Text Output
4. Save the flow
5. Enable "MCP Server" in flow settings

**Register Langflow with MCP Gateway:**

```bash
curl -X POST http://localhost:4444/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "langflow-tools",
    "url": "http://localhost:7860/mcp",
    "description": "Langflow AI workflows"
  }'
```

### Step 6: Verify Complete Setup

```bash
# List all registered servers
curl http://localhost:4444/servers | jq

# List all available tools
curl http://localhost:4444/mcp/tools | jq

# Expected: You should see tools from all registered servers
```

---

## Demo 1: Simple Research Assistant

**Goal**: Create a simple agent that uses multiple tools through the gateway.

### Code

```python
# demo1_simple_research.py
from crewai import Agent, Task, Crew

# Create research agent
researcher = Agent(
    role="Research Assistant",
    goal="Answer questions using available tools",
    backstory="You are a helpful research assistant with access to web search and knowledge bases.",
    mcps=[{
        "name": "contextforge",
        "url": "http://localhost:4444/mcp"
    }],
    verbose=True
)

# Create research task
task = Task(
    description="What are the latest developments in quantum computing?",
    expected_output="A comprehensive summary with sources",
    agent=researcher
)

# Create and run crew
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=2
)

# Execute
result = crew.kickoff()

print("\n" + "="*80)
print("RESULT:")
print("="*80)
print(result)
```

### Run Demo 1

```bash
# Run the demo
python demo1_simple_research.py

# Expected: Agent will use web search and Wikipedia tools
# to research quantum computing and provide a summary
```

---

## Demo 2: Multi-Agent Research System

**Goal**: Create a sophisticated multi-agent system with specialization.

### Code

```python
# demo2_multi_agent_research.py
from crewai import Agent, Task, Crew, Process

MCP_GATEWAY = "http://localhost:4444/mcp"

# Create specialized agents
web_researcher = Agent(
    role="Web Research Specialist",
    goal="Find current information from web sources",
    backstory="Expert at web research and source evaluation",
    mcps=[{"name": "contextforge", "url": MCP_GATEWAY}],
    verbose=True
)

knowledge_analyst = Agent(
    role="Knowledge Base Analyst",
    goal="Extract information from encyclopedias and knowledge bases",
    backstory="Expert at synthesizing knowledge base information",
    mcps=[{"name": "contextforge", "url": MCP_GATEWAY}],
    verbose=True
)

report_writer = Agent(
    role="Technical Writer",
    goal="Create comprehensive research reports",
    backstory="Expert technical writer with strong analytical skills",
    mcps=[{"name": "contextforge", "url": MCP_GATEWAY}],
    verbose=True,
    allow_delegation=True
)

# Define research topic
TOPIC = "Artificial Intelligence in Healthcare"

# Create tasks
web_research_task = Task(
    description=f"Search the web for recent developments in {TOPIC}. Find 5-7 credible sources.",
    expected_output="List of sources with URLs and summaries",
    agent=web_researcher
)

knowledge_task = Task(
    description=f"Research {TOPIC} using Wikipedia and knowledge bases for background information.",
    expected_output="Comprehensive background summary",
    agent=knowledge_analyst
)

report_task = Task(
    description=f"Create a research report on {TOPIC} using all gathered information.",
    expected_output="Professional research report with citations",
    agent=report_writer,
    context=[web_research_task, knowledge_task]
)

# Create crew
research_crew = Crew(
    agents=[web_researcher, knowledge_analyst, report_writer],
    tasks=[web_research_task, knowledge_task, report_task],
    process=Process.sequential,
    verbose=2
)

# Execute
print(f"Starting research on: {TOPIC}")
result = research_crew.kickoff()

# Save report
with open(f"research_report_{TOPIC.replace(' ', '_')}.md", "w") as f:
    f.write(result)

print(f"\n✓ Report saved to: research_report_{TOPIC.replace(' ', '_')}.md")
```

### Run Demo 2

```bash
# Run multi-agent research
python demo2_multi_agent_research.py

# This will take a few minutes as agents collaborate
# Expected output: A comprehensive research report
```

---

## Demo 3: Customer Support Automation

**Goal**: Automate customer support ticket processing.

### Setup

```bash
# Create sample support data
cat > support_tickets.json <<EOF
{
  "tickets": [
    {
      "id": "TICK-001",
      "customer_id": "CUST-12345",
      "subject": "Cannot login after password reset",
      "description": "I reset my password but still cannot log in",
      "priority": "high"
    },
    {
      "id": "TICK-002",
      "customer_id": "CUST-67890",
      "subject": "Billing question about invoice",
      "description": "I was charged twice this month",
      "priority": "medium"
    }
  ]
}
EOF
```

### Code

```python
# demo3_customer_support.py
from crewai import Agent, Task, Crew, Process
import json

MCP_GATEWAY = "http://localhost:4444/mcp"

def process_support_ticket(ticket):
    # Create support agents
    classifier = Agent(
        role="Ticket Classifier",
        goal="Classify and prioritize support tickets",
        mcps=[{"name": "contextforge", "url": MCP_GATEWAY}],
        verbose=True
    )

    kb_specialist = Agent(
        role="Knowledge Base Specialist",
        goal="Find solutions in knowledge base",
        mcps=[{"name": "contextforge", "url": MCP_GATEWAY}],
        verbose=True
    )

    response_writer = Agent(
        role="Support Response Writer",
        goal="Generate professional support responses",
        mcps=[{"name": "contextforge", "url": MCP_GATEWAY}],
        verbose=True
    )

    # Create tasks
    classify_task = Task(
        description=f"Classify this ticket:\n{ticket['subject']}\n{ticket['description']}",
        expected_output="Classification and priority",
        agent=classifier
    )

    kb_search_task = Task(
        description=f"Find solutions for: {ticket['subject']}",
        expected_output="Relevant KB articles and solutions",
        agent=kb_specialist,
        context=[classify_task]
    )

    response_task = Task(
        description=f"Generate support response for ticket {ticket['id']}",
        expected_output="Complete email response",
        agent=response_writer,
        context=[classify_task, kb_search_task]
    )

    # Create crew
    support_crew = Crew(
        agents=[classifier, kb_specialist, response_writer],
        tasks=[classify_task, kb_search_task, response_task],
        process=Process.sequential,
        verbose=2
    )

    return support_crew.kickoff()

# Load and process tickets
with open("support_tickets.json") as f:
    data = json.load(f)

for ticket in data["tickets"]:
    print(f"\n{'='*80}")
    print(f"Processing Ticket: {ticket['id']}")
    print(f"{'='*80}")

    response = process_support_ticket(ticket)

    print(f"\n✓ Generated response for {ticket['id']}")
    print(response)
```

### Run Demo 3

```bash
# Run support automation
python demo3_customer_support.py

# Expected: Automated responses for each ticket
```

---

## Monitoring and Observability

### View MCP Gateway Logs

```bash
# Real-time logs
docker-compose logs -f gateway

# Search logs
docker-compose logs gateway | grep "tool_call"
```

### Monitor Tool Usage

```bash
# Get tool usage statistics
curl http://localhost:4444/stats/tools | jq

# Monitor active requests
curl http://localhost:4444/stats/active | jq
```

### Langflow Monitoring

Access Langflow UI at http://localhost:7860 to:
- View flow execution history
- Monitor performance metrics
- Debug flow issues

---

## Troubleshooting

### Issue 1: Gateway not starting

```bash
# Check logs
docker-compose logs gateway

# Common fix: Database not ready
docker-compose restart postgres gateway
sleep 10
curl http://localhost:4444/health
```

### Issue 2: Tools not discovered

```bash
# Refresh server registry
curl -X POST http://localhost:4444/servers/refresh

# Check individual server
curl -X GET http://localhost:4444/servers/langflow-tools

# Re-register server
curl -X DELETE http://localhost:4444/servers/langflow-tools
curl -X POST http://localhost:4444/servers \
  -H "Content-Type: application/json" \
  -d '{"name":"langflow-tools","url":"http://localhost:7860/mcp"}'
```

### Issue 3: CrewAI timeout

```python
# Increase timeout in agent configuration
agent = Agent(
    role="Researcher",
    mcps=[{
        "name": "contextforge",
        "url": "http://localhost:4444/mcp",
        "timeout": 60000  # 60 seconds
    }]
)
```

### Issue 4: Langflow flow not responding

```bash
# Restart Langflow
pkill -f langflow
langflow run --host 0.0.0.0 --port 7860 &

# Check Langflow health
curl http://localhost:7860/health
```

---

## Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Deactivate Python environment
deactivate
```

---

## Next Steps

1. **Explore More Use Cases**: See `/docs/use-cases/` for industry-specific examples
2. **Production Deployment**: Review `/docs/guides/` for production best practices
3. **Custom Integrations**: Learn to build custom MCP servers
4. **Advanced Langflow**: Create complex multi-step workflows

---

## Resources

- [Full Documentation](./guides/MCP-CrewAI-Langflow-Integration-Guide.md)
- [Use Cases](./use-cases/MCP-Gateway-Use-Cases-Solutions.md)
- [Code Examples](./examples/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [CrewAI Docs](https://docs.crewai.com/)
- [Langflow Docs](https://docs.langflow.org/)

---

**Questions or Issues?**

- Create an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Copyright 2025 Ruslan Magana**
**Licensed under Apache License 2.0**
