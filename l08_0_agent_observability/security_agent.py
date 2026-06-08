"""
Instrumented Security Agent

This agent demonstrates observability by tracing:
- Agent invocations
- Tool calls
- LLM API calls (simulated)
- Timing information
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from tracer import get_tracer


def create_instrumented_agent():
    """
    Create a security agent with Google Search tool.

    The agent can answer security questions using web search.
    """
    agent = LlmAgent(
        name="security_agent_traced",
        model="gemini-2.5-flash",
        description="Web security expert with search capabilities.",
        instruction="""You are a web security expert assistant. Your job is to help users
understand security threats, vulnerabilities, and best practices.

When answering questions:
1. Use the google_search tool to find current information
2. Provide clear, actionable security advice
3. Cite sources when possible
4. Explain technical concepts clearly

Focus on practical security guidance that helps protect users and systems.""",
        tools=[google_search]
    )

    return agent


if __name__ == "__main__":
    print("Testing instrumented security agent...")
    print("This will create trace files in the 'traces/' directory")
    print()

    agent = create_instrumented_agent()
    print(f"✓ Created agent: {agent.name}")
    print(f"✓ Tools available: {len(agent.tools)}")
    print()
    print("To run the agent with tracing, use: python run_agent.py")
