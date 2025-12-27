# Documentation: MCP Gateway with CrewAI and Langflow

Welcome to the comprehensive documentation for integrating MCP Context Forge Gateway with CrewAI and Langflow to build production-ready agentic AI systems.

## 📚 Documentation Structure

### 📖 Guides

**Main Integration Guide**
- [MCP-CrewAI-Langflow Integration Guide](./guides/MCP-CrewAI-Langflow-Integration-Guide.md)
  - Complete production-ready developer guide
  - Core concepts and architecture
  - Quickstart and configuration
  - End-to-end examples
  - Production hardening
  - Troubleshooting

**Langflow Integration**
- [Langflow MCP Integration Guide](./examples/langflow-mcp-integration-guide.md)
  - Langflow as MCP Server
  - Langflow as MCP Client
  - Advanced use cases
  - Best practices

### 💼 Use Cases and Solutions

**[Use Cases Guide](./use-cases/MCP-Gateway-Use-Cases-Solutions.md)**

Industry-specific implementations:

1. **Enterprise Use Cases**
   - Intelligent Research Assistant
   - Customer Support Automation
   - Content Marketing Pipeline

2. **Research and Analysis**
   - Market Intelligence Platform
   - Financial Research Automation

3. **DevOps and Automation**
   - Intelligent Incident Response
   - Infrastructure Management

Each use case includes:
- Business problem statement
- Solution architecture
- Complete implementation code
- ROI metrics

### 🎯 Demo Guide

**[Complete Demo Guide](./DEMO-GUIDE.md)**

Step-by-step instructions for running demos:

- **Demo 1**: Simple Research Assistant
- **Demo 2**: Multi-Agent Research System
- **Demo 3**: Customer Support Automation

Includes:
- Prerequisites and setup
- Complete code examples
- Running instructions
- Monitoring and troubleshooting

### 💻 Code Examples

**CrewAI Examples**
- [Research Assistant Example](./examples/crewai-mcp-gateway-example.py)
  - Multi-agent research workflow
  - Tool federation through MCP Gateway
  - Report generation

- [Customer Support Example](./examples/crewai-customer-support-example.py)
  - Automated ticket processing
  - CRM and knowledge base integration
  - Response generation

**Langflow Examples**
- See [Langflow Integration Guide](./examples/langflow-mcp-integration-guide.md) for flow configurations

### 📄 Additional Resources

**Production Guide (Word Document)**
- [ContextForge MCP Gateway Pro Guide.docx](./ContextForge_MCP_Gateway_Pro_Guide.docx)
  - Comprehensive Word document for printing/sharing
  - Same content as markdown guides
  - Professional formatting

**Generation Script**
- [generate_pro_guide.py](./generate_pro_guide.py)
  - Script to regenerate Word documentation
  - Customize and regenerate as needed

## 🚀 Quick Start

### 1. Read the Main Guide

Start with the [MCP-CrewAI-Langflow Integration Guide](./guides/MCP-CrewAI-Langflow-Integration-Guide.md) to understand:
- Core concepts (Agentic AI, MCP, Gateway)
- Architecture and request flow
- Configuration best practices

### 2. Run a Demo

Follow the [Demo Guide](./DEMO-GUIDE.md) to:
- Set up your environment
- Run complete working examples
- Understand the integration patterns

### 3. Explore Use Cases

Review [Use Cases and Solutions](./use-cases/MCP-Gateway-Use-Cases-Solutions.md) to:
- Find industry-specific examples
- Understand ROI and business impact
- Get implementation templates

### 4. Build Your Solution

Use the code examples in `/examples/` to:
- Build custom agents
- Create workflows
- Integrate with your systems

## 📋 Learning Paths

### Path 1: For Developers (New to MCP)

1. Read sections 1-3 of the Integration Guide (concepts and architecture)
2. Run Demo 1 (Simple Research Assistant)
3. Study the CrewAI Research Example
4. Explore the Langflow Integration Guide
5. Build your first custom agent

### Path 2: For Platform Engineers

1. Read sections 4-5 of the Integration Guide (setup and configuration)
2. Review the Production Hardening section (section 9)
3. Study the DevOps use case (Incident Response)
4. Set up monitoring and observability
5. Deploy to production environment

### Path 3: For Business Analysts

1. Review Use Cases and Solutions document
2. Read ROI metrics and business impact sections
3. Run Demo 2 (Multi-Agent Research)
4. Explore industry-specific examples
5. Define requirements for your use case

## 🔧 Prerequisites

Before diving into the documentation:

### Technical Requirements
- Python 3.10+
- Docker and Docker Compose
- Basic understanding of:
  - REST APIs
  - Async programming
  - AI/LLM concepts

### Required Accounts
- IBM Cloud (for WatsonX)
- Optional: Google Cloud (for Search API)

### Recommended Knowledge
- Familiarity with CrewAI or similar agent frameworks
- Understanding of workflow automation
- Basic DevOps/deployment experience

## 📖 Key Concepts Reference

### MCP (Model Context Protocol)
- Standard protocol for AI tool integration
- Enables tool discovery and invocation
- Supports multiple transports (HTTP, WebSocket, SSE)

### ContextForge MCP Gateway
- Federates multiple MCP servers
- Provides governance and observability
- Bridges legacy APIs to MCP

### CrewAI
- Multi-agent orchestration framework
- Supports MCP protocol natively
- Enables agent collaboration

### Langflow
- Visual workflow builder for AI
- Can act as MCP server and client
- Provides drag-and-drop flow creation

## 🎓 Additional Resources

### Official Documentation
- [MCP Specification](https://modelcontextprotocol.io/)
- [ContextForge Gateway](https://ibm.github.io/mcp-context-forge/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Langflow Documentation](https://docs.langflow.org/)

### Community Resources
- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share solutions
- Examples Repository: Community-contributed examples

## 🤝 Contributing

Found an error or want to improve the documentation?

1. Fork the repository
2. Make your changes
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## 📧 Support

- **Issues**: GitHub Issues
- **Questions**: GitHub Discussions
- **Email**: See main README.md for contact information

## 📝 Documentation Versions

- **Current Version**: 1.0.0
- **Last Updated**: 2025-12-27
- **Compatibility**:
  - ContextForge MCP Gateway: 1.x
  - CrewAI: 0.8+
  - Langflow: 1.0+

## 🔄 Keeping Documentation Updated

This documentation is actively maintained. To regenerate the Word document:

```bash
cd docs
python generate_pro_guide.py
```

---

## 📑 Documentation Index

### By Topic

**Getting Started**
- [Quick Start](./DEMO-GUIDE.md#setup-phase)
- [Prerequisites](./DEMO-GUIDE.md#prerequisites)
- [First Demo](./DEMO-GUIDE.md#demo-1-simple-research-assistant)

**Architecture**
- [Core Concepts](./guides/MCP-CrewAI-Langflow-Integration-Guide.md#2-core-concepts-agentic-ai-mcp-gateway)
- [Request Flow](./guides/MCP-CrewAI-Langflow-Integration-Guide.md#32-gateway-request-flow-mental-model)
- [Integration Patterns](./examples/langflow-mcp-integration-guide.md#architecture)

**Implementation**
- [CrewAI Examples](./examples/crewai-mcp-gateway-example.py)
- [Langflow Flows](./examples/langflow-mcp-integration-guide.md)
- [Use Case Templates](./use-cases/MCP-Gateway-Use-Cases-Solutions.md)

**Operations**
- [Configuration](./guides/MCP-CrewAI-Langflow-Integration-Guide.md#5-configuration-that-matters-in-production)
- [Production Hardening](./guides/MCP-CrewAI-Langflow-Integration-Guide.md#9-production-hardening-guide)
- [Troubleshooting](./DEMO-GUIDE.md#troubleshooting)

---

**Happy Building! 🚀**

For questions or feedback, please open an issue on GitHub.

---

**Copyright 2025 Ruslan Magana**
**Licensed under Apache License 2.0**
