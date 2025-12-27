"""
CrewAI Customer Support Automation with MCP Gateway

This example demonstrates a customer support automation system using CrewAI
and MCP Gateway to access multiple tools (CRM, knowledge base, ticketing).

Use Case: Automated customer inquiry handling with:
- Ticket classification
- Knowledge base search
- Customer history lookup
- Automated response generation

Prerequisites:
1. ContextForge MCP Gateway running
2. Customer support tools registered as MCP servers
3. CrewAI installed
"""

import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Optional

# Configuration
MCP_GATEWAY_URL = os.getenv("MCP_GATEWAY_URL", "http://localhost:4444/mcp")


class CustomerSupportCrew:
    """Customer support automation crew using MCP tools."""

    def __init__(self):
        """Initialize the customer support crew."""
        self.mcp_config = {
            "name": "contextforge",
            "url": MCP_GATEWAY_URL
        }

    def create_agents(self) -> List[Agent]:
        """Create specialized customer support agents."""

        # Agent 1: Ticket Classifier
        classifier = Agent(
            role="Support Ticket Classifier",
            goal="Accurately classify and prioritize incoming support tickets",
            backstory=(
                "You are an experienced support team lead who can quickly "
                "identify the type and urgency of customer issues. You use "
                "ticket analysis tools to categorize issues and determine priority."
            ),
            mcps=[self.mcp_config],
            verbose=True,
        )

        # Agent 2: Knowledge Base Specialist
        kb_specialist = Agent(
            role="Knowledge Base Specialist",
            goal="Find relevant solutions from knowledge base and documentation",
            backstory=(
                "You are a documentation expert who knows how to search and "
                "extract relevant information from knowledge bases, FAQs, "
                "and product documentation to solve customer issues."
            ),
            mcps=[self.mcp_config],
            verbose=True,
        )

        # Agent 3: Customer History Analyst
        history_analyst = Agent(
            role="Customer History Analyst",
            goal="Analyze customer history and previous interactions",
            backstory=(
                "You are a CRM specialist who analyzes customer history, "
                "previous tickets, and interaction patterns to provide "
                "personalized support."
            ),
            mcps=[self.mcp_config],
            verbose=True,
        )

        # Agent 4: Response Generator
        response_generator = Agent(
            role="Support Response Specialist",
            goal="Generate professional, helpful customer responses",
            backstory=(
                "You are an expert customer service representative who writes "
                "clear, empathetic, and solution-focused responses. You maintain "
                "brand voice and ensure customer satisfaction."
            ),
            mcps=[self.mcp_config],
            verbose=True,
        )

        # Agent 5: Quality Assurance
        qa_agent = Agent(
            role="Quality Assurance Specialist",
            goal="Review and improve customer support responses",
            backstory=(
                "You are a QA specialist who ensures all customer responses "
                "meet quality standards, are accurate, and properly address "
                "customer concerns."
            ),
            mcps=[self.mcp_config],
            verbose=True,
        )

        return [classifier, kb_specialist, history_analyst, response_generator, qa_agent]

    def handle_ticket(
        self,
        ticket_id: str,
        customer_id: str,
        subject: str,
        description: str,
        customer_email: str
    ) -> Dict:
        """
        Process a customer support ticket through the crew.

        Args:
            ticket_id: Unique ticket identifier
            customer_id: Customer identifier
            subject: Ticket subject
            description: Full ticket description
            customer_email: Customer's email address

        Returns:
            Dictionary containing processed ticket information
        """

        agents = self.create_agents()
        classifier, kb_specialist, history_analyst, response_generator, qa_agent = agents

        # Task 1: Classify the ticket
        classify_task = Task(
            description=(
                f"Classify the following support ticket:\n\n"
                f"Ticket ID: {ticket_id}\n"
                f"Subject: {subject}\n"
                f"Description: {description}\n\n"
                f"Determine:\n"
                f"- Category (Technical, Billing, Feature Request, Bug, Other)\n"
                f"- Priority (Critical, High, Medium, Low)\n"
                f"- Estimated complexity (Simple, Moderate, Complex)\n"
                f"- Required expertise (Level 1, Level 2, Specialist)\n"
                f"- Tags/keywords for knowledge base search"
            ),
            expected_output=(
                "A classification report with category, priority, complexity, "
                "required expertise, and relevant tags"
            ),
            agent=classifier,
        )

        # Task 2: Search knowledge base
        kb_search_task = Task(
            description=(
                f"Based on the ticket classification, search the knowledge base for "
                f"relevant solutions to:\n\n"
                f"Subject: {subject}\n"
                f"Description: {description}\n\n"
                f"Find:\n"
                f"- Existing solutions or workarounds\n"
                f"- Related documentation\n"
                f"- Similar resolved tickets\n"
                f"- Product guides or tutorials"
            ),
            expected_output=(
                "A list of relevant knowledge base articles, solutions, and "
                "documentation links with relevance scores"
            ),
            agent=kb_specialist,
            context=[classify_task],
        )

        # Task 3: Analyze customer history
        history_task = Task(
            description=(
                f"Retrieve and analyze the history for customer {customer_id}:\n\n"
                f"Look for:\n"
                f"- Previous tickets and their resolutions\n"
                f"- Account status and subscription level\n"
                f"- Recent interactions\n"
                f"- Known issues or patterns\n"
                f"- Customer satisfaction history\n\n"
                f"Use CRM tools to gather comprehensive customer context."
            ),
            expected_output=(
                "A customer profile summary including previous tickets, "
                "account status, and relevant history"
            ),
            agent=history_analyst,
        )

        # Task 4: Generate response
        response_task = Task(
            description=(
                f"Generate a professional support response for ticket {ticket_id}.\n\n"
                f"Original ticket:\n"
                f"Subject: {subject}\n"
                f"Description: {description}\n\n"
                f"Use the classification, knowledge base results, and customer history "
                f"to create a response that:\n"
                f"- Addresses the customer's issue directly\n"
                f"- Provides clear step-by-step solutions\n"
                f"- Is personalized based on customer history\n"
                f"- Maintains professional and empathetic tone\n"
                f"- Includes relevant links and resources\n"
                f"- Sets appropriate expectations for resolution"
            ),
            expected_output=(
                "A complete email response to the customer, including greeting, "
                "solution, resources, and signature"
            ),
            agent=response_generator,
            context=[classify_task, kb_search_task, history_task],
        )

        # Task 5: Quality check
        qa_task = Task(
            description=(
                f"Review the generated response for ticket {ticket_id}.\n\n"
                f"Check:\n"
                f"- Accuracy of information\n"
                f"- Completeness of solution\n"
                f"- Tone and professionalism\n"
                f"- Proper links and resources\n"
                f"- Grammar and formatting\n"
                f"- Alignment with brand guidelines\n\n"
                f"Provide:\n"
                f"- Approval or revision recommendations\n"
                f"- Quality score (1-10)\n"
                f"- Suggested improvements if needed"
            ),
            expected_output=(
                "A QA report with approval status, quality score, and "
                "any recommended improvements"
            ),
            agent=qa_agent,
            context=[response_task],
        )

        # Create and run the crew
        crew = Crew(
            agents=agents,
            tasks=[classify_task, kb_search_task, history_task, response_task, qa_task],
            process=Process.sequential,
            verbose=2,
        )

        result = crew.kickoff()

        return {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "processed_at": datetime.now().isoformat(),
            "result": result
        }


def main():
    """Main execution function with example tickets."""

    print("=" * 80)
    print("Customer Support Automation with CrewAI + MCP Gateway")
    print("=" * 80)
    print()

    support_crew = CustomerSupportCrew()

    # Example ticket 1: Technical issue
    print("\n--- Processing Ticket 1: Technical Issue ---\n")
    ticket1 = support_crew.handle_ticket(
        ticket_id="TICK-2025-001",
        customer_id="CUST-12345",
        subject="Unable to login after password reset",
        description=(
            "I reset my password 30 minutes ago using the 'Forgot Password' link, "
            "but I still cannot log in. I've tried multiple times with the new password "
            "and keep getting 'Invalid credentials' error. I need to access my account "
            "urgently for an important presentation."
        ),
        customer_email="john.doe@example.com"
    )

    print("\n--- Ticket 1 Result ---")
    print(ticket1)

    # Example ticket 2: Billing inquiry
    print("\n\n--- Processing Ticket 2: Billing Inquiry ---\n")
    ticket2 = support_crew.handle_ticket(
        ticket_id="TICK-2025-002",
        customer_id="CUST-67890",
        subject="Unexpected charge on my account",
        description=(
            "I noticed a charge of $99.99 on my credit card for 'Premium Subscription' "
            "but I only signed up for the Basic plan at $29.99/month. I've been charged "
            "the higher amount for the last two months. Can you please explain this "
            "and issue a refund?"
        ),
        customer_email="jane.smith@example.com"
    )

    print("\n--- Ticket 2 Result ---")
    print(ticket2)


if __name__ == "__main__":
    main()
