"""
CrewAI + MCP Gateway Integration Example

This example demonstrates how to build a multi-agent research system using CrewAI
connected to the ContextForge MCP Gateway for tool federation.

Prerequisites:
1. ContextForge MCP Gateway running (http://localhost:4444)
2. MCP servers registered (search, wikipedia, langflow tools)
3. CrewAI installed: pip install crewai crewai-tools

Architecture:
- CrewAI agents connect to ContextForge MCP Gateway
- Gateway federates multiple MCP servers (search, wikipedia, langflow)
- Agents use tools transparently without knowing backend details
"""

import os
from crewai import Agent, Task, Crew, Process
from typing import Optional

# Configuration
MCP_GATEWAY_URL = os.getenv("MCP_GATEWAY_URL", "http://localhost:4444/mcp")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")


def create_research_crew(topic: str) -> Crew:
    """
    Create a research crew with multiple specialized agents.

    Args:
        topic: Research topic

    Returns:
        Configured Crew instance
    """

    # Agent 1: Web Researcher
    # Uses search tools to find recent, relevant information
    web_researcher = Agent(
        role="Web Research Specialist",
        goal=f"Find the most recent and relevant information about {topic} from web sources",
        backstory=(
            "You are an expert web researcher with a keen eye for credible sources. "
            "You know how to craft effective search queries and evaluate source quality. "
            "You always cite your sources with URLs and publication dates."
        ),
        mcps=[{
            "name": "contextforge",
            "url": MCP_GATEWAY_URL
        }],
        verbose=True,
        allow_delegation=False,
    )

    # Agent 2: Knowledge Base Analyst
    # Uses Wikipedia and other knowledge base tools
    knowledge_analyst = Agent(
        role="Knowledge Base Analyst",
        goal=f"Extract foundational knowledge and background information about {topic}",
        backstory=(
            "You are a knowledge management expert who excels at synthesizing "
            "information from encyclopedias and knowledge bases. You provide "
            "well-structured background information with proper context."
        ),
        mcps=[{
            "name": "contextforge",
            "url": MCP_GATEWAY_URL
        }],
        verbose=True,
        allow_delegation=False,
    )

    # Agent 3: Data Synthesizer
    # Uses Langflow tools for advanced analysis and synthesis
    data_synthesizer = Agent(
        role="Data Synthesis Expert",
        goal=f"Synthesize research findings into actionable insights about {topic}",
        backstory=(
            "You are a data scientist and technical writer who excels at creating "
            "executive summaries. You transform raw research into clear, actionable "
            "insights with proper citations and visualizations where appropriate."
        ),
        mcps=[{
            "name": "contextforge",
            "url": MCP_GATEWAY_URL
        }],
        verbose=True,
        allow_delegation=False,
    )

    # Agent 4: Report Writer
    # Coordinates all findings into a final report
    report_writer = Agent(
        role="Technical Report Writer",
        goal=f"Create a comprehensive, publication-ready report on {topic}",
        backstory=(
            "You are an experienced technical writer and editor. You create "
            "well-structured, clear, and engaging reports that communicate complex "
            "information to diverse audiences. You ensure all claims are backed by citations."
        ),
        mcps=[{
            "name": "contextforge",
            "url": MCP_GATEWAY_URL
        }],
        verbose=True,
        allow_delegation=True,
    )

    # Task 1: Web Research
    task_web_research = Task(
        description=(
            f"Use web search tools to find 8-10 high-quality, recent sources about {topic}. "
            "Focus on:\n"
            "- Recent developments (last 6-12 months)\n"
            "- Credible sources (academic papers, industry reports, tech news)\n"
            "- Diverse perspectives\n\n"
            "For each source, provide:\n"
            "- Full URL\n"
            "- Publication date\n"
            "- 2-3 sentence summary\n"
            "- Relevance score (1-10)"
        ),
        expected_output=(
            "A structured list of 8-10 sources with URLs, dates, summaries, and relevance scores"
        ),
        agent=web_researcher,
    )

    # Task 2: Knowledge Base Research
    task_knowledge_research = Task(
        description=(
            f"Use Wikipedia and knowledge base tools to gather foundational information about {topic}. "
            "Focus on:\n"
            "- Historical context and evolution\n"
            "- Key concepts and terminology\n"
            "- Major players and organizations\n"
            "- Related technologies or fields\n\n"
            "Structure the information with clear sections and include all citations."
        ),
        expected_output=(
            "A well-structured knowledge base summary with sections for history, concepts, "
            "key players, and related fields. All facts must be cited."
        ),
        agent=knowledge_analyst,
    )

    # Task 3: Data Synthesis
    task_synthesis = Task(
        description=(
            f"Synthesize the web research and knowledge base findings about {topic}. "
            "Use advanced analysis tools (Langflow) to:\n"
            "- Identify key trends and patterns\n"
            "- Extract actionable insights\n"
            "- Highlight contradictions or gaps\n"
            "- Create data visualizations if possible\n\n"
            "Focus on what decision-makers need to know."
        ),
        expected_output=(
            "An executive summary with:\n"
            "- 3-5 key trends\n"
            "- 5-7 actionable insights\n"
            "- List of knowledge gaps or uncertainties\n"
            "- Recommendations for further investigation"
        ),
        agent=data_synthesizer,
        context=[task_web_research, task_knowledge_research],
    )

    # Task 4: Final Report
    task_final_report = Task(
        description=(
            f"Create a comprehensive, publication-ready report on {topic}. "
            "The report must include:\n\n"
            "1. Executive Summary (1 page)\n"
            "2. Background and Context (1-2 pages)\n"
            "3. Current State Analysis (2-3 pages)\n"
            "4. Key Trends and Insights (2-3 pages)\n"
            "5. Recommendations (1 page)\n"
            "6. References (complete bibliography)\n\n"
            "Use clear headings, bullet points, and professional formatting. "
            "Ensure all claims are properly cited."
        ),
        expected_output=(
            "A 8-12 page professional research report in markdown format with "
            "proper structure, citations, and formatting"
        ),
        agent=report_writer,
        context=[task_web_research, task_knowledge_research, task_synthesis],
    )

    # Create and return the crew
    crew = Crew(
        agents=[web_researcher, knowledge_analyst, data_synthesizer, report_writer],
        tasks=[task_web_research, task_knowledge_research, task_synthesis, task_final_report],
        process=Process.sequential,
        verbose=2,
    )

    return crew


def create_simple_crew(query: str) -> Crew:
    """
    Create a simple single-agent crew for quick queries.

    Args:
        query: Question or task to execute

    Returns:
        Configured Crew instance
    """

    assistant = Agent(
        role="AI Assistant",
        goal=f"Answer the query: {query}",
        backstory=(
            "You are a helpful AI assistant with access to various tools. "
            "You provide accurate, well-researched answers with proper citations."
        ),
        mcps=[{
            "name": "contextforge",
            "url": MCP_GATEWAY_URL
        }],
        verbose=True,
    )

    task = Task(
        description=query,
        expected_output="A clear, comprehensive answer with citations",
        agent=assistant,
    )

    crew = Crew(
        agents=[assistant],
        tasks=[task],
        process=Process.sequential,
        verbose=2,
    )

    return crew


def main():
    """Main execution function."""

    print("=" * 80)
    print("CrewAI + MCP Gateway Integration Demo")
    print("=" * 80)
    print()

    # Example 1: Simple query
    print("\n--- Example 1: Simple Query ---\n")
    simple_query = "What are the latest developments in quantum computing?"
    simple_crew = create_simple_crew(simple_query)

    try:
        result = simple_crew.kickoff()
        print("\n--- Result ---")
        print(result)
    except Exception as e:
        print(f"Error: {e}")

    # Example 2: Complex research project
    print("\n\n--- Example 2: Complex Research Project ---\n")
    research_topic = "Artificial Intelligence in Healthcare"
    research_crew = create_research_crew(research_topic)

    try:
        result = research_crew.kickoff()
        print("\n--- Final Report ---")
        print(result)

        # Save report to file
        output_file = f"research_report_{research_topic.replace(' ', '_').lower()}.md"
        with open(output_file, "w") as f:
            f.write(result)
        print(f"\n✓ Report saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
