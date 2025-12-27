# Langflow + MCP Gateway Integration Guide

This guide demonstrates how to integrate Langflow with the ContextForge MCP Gateway to create powerful, reusable AI workflows.

## Overview

Langflow can work with MCP Gateway in two ways:

1. **Langflow as MCP Server**: Expose Langflow flows as MCP tools
2. **Langflow as MCP Client**: Use MCP tools inside Langflow flows

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   AI Applications                            │
│              (CrewAI, LangChain, Custom)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              ContextForge MCP Gateway                        │
│           (Tool Federation & Governance)                     │
└─────┬──────────────┬──────────────┬──────────────────┬──────┘
      │              │              │                  │
┌─────▼────┐  ┌──────▼────┐  ┌─────▼──────┐  ┌───────▼────────┐
│ Search   │  │ Wikipedia │  │  Database  │  │  Langflow      │
│ Tools    │  │   Tools   │  │   Tools    │  │  Flows (MCP)   │
└──────────┘  └───────────┘  └────────────┘  └────────────────┘
                                                      │
                                              ┌───────▼────────┐
                                              │  Langflow also │
                                              │  uses MCP tools│
                                              └────────────────┘
```

## Part 1: Langflow as MCP Server

### Step 1: Install and Run Langflow

```bash
# Install Langflow
pip install langflow

# Run Langflow
langflow run --host 0.0.0.0 --port 7860

# Access UI at http://localhost:7860
```

### Step 2: Create a Flow in Langflow

Example flow: **Document Summarizer with Citation Extraction**

**Flow Components:**

1. **Input Component**: Text input (document URL or text)
2. **URL Loader**: Fetch content from URL
3. **Text Splitter**: Split document into chunks
4. **Embeddings**: Create embeddings for chunks
5. **Vector Store**: Store embeddings
6. **LLM**: Summarization model
7. **Prompt Template**: Summarization prompt
8. **Citation Extractor**: Custom component to extract citations
9. **Output Component**: Structured output

**Flow Configuration (JSON representation):**

```json
{
  "name": "Document Summarizer",
  "description": "Summarizes documents and extracts citations",
  "nodes": [
    {
      "id": "input_1",
      "type": "TextInput",
      "data": {
        "name": "document_url",
        "description": "URL of document to summarize"
      }
    },
    {
      "id": "url_loader_1",
      "type": "URLLoader",
      "data": {
        "url": "{input_1}"
      }
    },
    {
      "id": "splitter_1",
      "type": "RecursiveCharacterTextSplitter",
      "data": {
        "chunk_size": 1000,
        "chunk_overlap": 200
      }
    },
    {
      "id": "llm_1",
      "type": "OpenAI",
      "data": {
        "model_name": "gpt-4",
        "temperature": 0.3
      }
    },
    {
      "id": "prompt_1",
      "type": "PromptTemplate",
      "data": {
        "template": "Summarize the following document and extract all citations:\n\n{text}\n\nProvide:\n1. Executive summary (3-5 sentences)\n2. Key points (bullet list)\n3. All citations found in the document"
      }
    },
    {
      "id": "output_1",
      "type": "Output",
      "data": {
        "name": "summary_result"
      }
    }
  ]
}
```

### Step 3: Enable MCP Server Mode

In Langflow UI:

1. Click on the flow settings (gear icon)
2. Navigate to **"MCP Server"** tab
3. Enable **"Expose as MCP Server"**
4. Configure MCP settings:
   - **Tool Name**: `summarize_document`
   - **Description**: "Summarizes documents and extracts citations"
   - **Input Schema**: Auto-generated from flow inputs
   - **Output Schema**: Auto-generated from flow outputs

### Step 4: Register Langflow with MCP Gateway

```bash
# Register Langflow as an MCP server
curl -X POST http://localhost:4444/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "langflow-tools",
    "url": "http://localhost:7860/mcp",
    "description": "Langflow AI workflows as MCP tools",
    "health_check_path": "/health",
    "timeout": 30000
  }'

# Verify registration
curl http://localhost:4444/servers

# Test tool discovery
curl http://localhost:4444/mcp/tools
```

### Step 5: Use Langflow Tools from Any MCP Client

**Example: Python MCP Client**

```python
import requests

# Call Langflow tool via MCP Gateway
response = requests.post(
    "http://localhost:4444/mcp/call_tool",
    json={
        "tool": "summarize_document",
        "arguments": {
            "document_url": "https://arxiv.org/pdf/2103.14030.pdf"
        }
    }
)

result = response.json()
print(result)
```

**Example: CrewAI Agent**

```python
from crewai import Agent, Task, Crew

analyst = Agent(
    role="Research Analyst",
    goal="Summarize research papers",
    mcps=[{"name": "contextforge", "url": "http://localhost:4444/mcp"}],
    verbose=True
)

task = Task(
    description="Summarize the paper at https://arxiv.org/pdf/2103.14030.pdf",
    expected_output="A summary with key points and citations",
    agent=analyst
)

crew = Crew(agents=[analyst], tasks=[task])
result = crew.kickoff()
```

## Part 2: Langflow as MCP Client

### Step 1: Add MCP Tools Component to Langflow

1. Open Langflow UI
2. Create a new flow
3. Add **"MCP Tools"** component from the sidebar
4. Configure the MCP server connection

### Step 2: Configure MCP Connection

**MCP Tools Component Configuration:**

```yaml
Component: MCP Tools
Settings:
  - MCP Server URL: http://localhost:4444/mcp
  - Authentication: Bearer token (optional)
  - Available Tools: Auto-discovered from gateway
  - Tool Selection: Choose which tools to use in this flow
```

### Step 3: Create a Flow Using MCP Tools

**Example Flow: Research Report Generator**

**Components:**

1. **Text Input**: Research topic
2. **MCP Tools - Web Search**: Search for recent articles
3. **MCP Tools - Wikipedia**: Get background information
4. **Data Aggregator**: Combine search results
5. **LLM**: Generate report
6. **Output**: Final report

**Flow Diagram:**

```
[Input: Topic]
      │
      ├──→ [MCP: Web Search] ──→ [Results: Articles]
      │                                │
      └──→ [MCP: Wikipedia] ──→ [Results: Background]
                                       │
                    [Combine Results] ←┘
                           │
                    [LLM: Generate Report]
                           │
                    [Output: Final Report]
```

### Step 4: Example Flow Implementation

**Python Code to Create the Flow Programmatically:**

```python
from langflow import Flow, Component

# Create flow
flow = Flow(name="Research Report Generator")

# Input component
topic_input = Component(
    type="TextInput",
    name="research_topic",
    description="Topic to research"
)

# MCP Tools: Web Search
web_search = Component(
    type="MCPTools",
    name="web_search",
    config={
        "server_url": "http://localhost:4444/mcp",
        "tool_name": "web_search",
        "arguments": {
            "query": "{research_topic}",
            "num_results": 10
        }
    }
)

# MCP Tools: Wikipedia
wikipedia = Component(
    type="MCPTools",
    name="wikipedia_search",
    config={
        "server_url": "http://localhost:4444/mcp",
        "tool_name": "wikipedia_summary",
        "arguments": {
            "topic": "{research_topic}",
            "sentences": 10
        }
    }
)

# Combine results
combiner = Component(
    type="DataAggregator",
    name="combine_results",
    inputs=[web_search.output, wikipedia.output]
)

# LLM for report generation
llm = Component(
    type="OpenAI",
    name="report_generator",
    config={
        "model": "gpt-4",
        "temperature": 0.7,
        "prompt": """
        Create a comprehensive research report on {research_topic}.

        Use the following sources:

        Web Research:
        {web_search_results}

        Background Knowledge:
        {wikipedia_results}

        Generate a report with:
        1. Executive Summary
        2. Background
        3. Current State
        4. Key Findings
        5. References
        """
    }
)

# Output
output = Component(
    type="Output",
    name="final_report",
    input=llm.output
)

# Connect components
flow.add_components([
    topic_input,
    web_search,
    wikipedia,
    combiner,
    llm,
    output
])

# Save flow
flow.save("research_report_generator.json")
```

## Part 3: Advanced Use Cases

### Use Case 1: Multi-Tool Research Pipeline

**Scenario**: Combine multiple MCP tools for comprehensive research

**Tools Used**:
- Web search
- Wikipedia
- Database query
- PDF extraction
- Langflow summarization

**Flow**:
```
Topic → [Search] → URLs
     → [Wikipedia] → Background
     → [Database] → Historical data
     → [PDF Extract] → Papers
            ↓
     [Summarize All]
            ↓
     [Generate Report]
```

### Use Case 2: Customer Support Automation

**Scenario**: Automated ticket resolution using multiple data sources

**Tools Used**:
- CRM lookup (MCP)
- Knowledge base search (MCP)
- Ticket classification (Langflow)
- Response generation (Langflow)

**Flow**:
```
Ticket → [Classify] → Category
      → [MCP: CRM] → Customer history
      → [MCP: KB] → Solutions
            ↓
     [Generate Response]
            ↓
     [Quality Check]
```

### Use Case 3: Data Processing Pipeline

**Scenario**: Extract, transform, and analyze data from multiple sources

**Tools Used**:
- API data fetch (MCP)
- Database query (MCP)
- Data transformation (Langflow)
- Analytics (Langflow)
- Visualization (MCP)

## Best Practices

### 1. Tool Naming and Organization

```bash
# Use clear, descriptive names
✓ "langflow-document-summarizer"
✗ "lf-tool-1"

# Group related tools
✓ "langflow-research-*"
  - langflow-research-summarizer
  - langflow-research-citation-extractor
  - langflow-research-fact-checker
```

### 2. Error Handling

```python
# In Langflow flows, add error handling components
try_catch = Component(
    type="TryCatch",
    try_block=[web_search, wikipedia],
    catch_block=[fallback_response],
    finally_block=[cleanup]
)
```

### 3. Caching and Performance

```python
# Configure caching in MCP Gateway
curl -X PATCH http://localhost:4444/servers/langflow-tools \
  -H "Content-Type: application/json" \
  -d '{
    "cache_ttl": 3600,
    "rate_limit": {
      "requests_per_minute": 60
    }
  }'
```

### 4. Monitoring and Observability

```python
# Enable telemetry for Langflow tools
# In Langflow settings
{
  "telemetry": {
    "enabled": true,
    "endpoint": "http://localhost:4444/telemetry",
    "trace_sampling": 0.1
  }
}
```

## Troubleshooting

### Issue 1: Langflow MCP Server Not Responding

**Solution**:
```bash
# Check Langflow status
curl http://localhost:7860/health

# Check MCP endpoint
curl http://localhost:7860/mcp/tools

# Restart Langflow with debug logging
langflow run --host 0.0.0.0 --port 7860 --log-level debug
```

### Issue 2: Tools Not Appearing in MCP Gateway

**Solution**:
```bash
# Verify server registration
curl http://localhost:4444/servers/langflow-tools

# Force refresh
curl -X POST http://localhost:4444/servers/langflow-tools/refresh

# Check gateway logs
docker logs mcp-gateway
```

### Issue 3: Authentication Failures

**Solution**:
```bash
# Update server with auth credentials
curl -X PATCH http://localhost:4444/servers/langflow-tools \
  -H "Content-Type: application/json" \
  -d '{
    "auth": {
      "type": "bearer",
      "token": "your-langflow-api-key"
    }
  }'
```

## Next Steps

1. **Explore Pre-built Flows**: Check Langflow Hub for community flows
2. **Create Custom Components**: Build specialized Langflow components
3. **Scale Production**: Deploy Langflow with Kubernetes
4. **Monitor Performance**: Set up observability dashboards
5. **Optimize Costs**: Implement caching and rate limiting

## Resources

- [Langflow Documentation](https://docs.langflow.org/)
- [Langflow MCP Server Guide](https://docs.langflow.org/mcp-server)
- [Langflow MCP Client Guide](https://docs.langflow.org/mcp-client)
- [MCP Specification](https://modelcontextprotocol.io/)
- [ContextForge Gateway Docs](https://ibm.github.io/mcp-context-forge/)

---

**Copyright 2025 Ruslan Magana**
**Licensed under Apache License 2.0**
