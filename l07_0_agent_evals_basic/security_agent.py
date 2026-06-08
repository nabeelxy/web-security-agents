"""
Security Assessment Agent

A simple security agent that provides domain safety assessments.
This agent will be evaluated for accuracy and consistency.
"""

from google.adk.agents import LlmAgent


def create_security_agent():
    """
    Create a security assessment agent.

    This agent answers questions about domain safety using its knowledge
    and reasoning capabilities. It does NOT use external tools - just
    in-context learning.

    Returns:
        LlmAgent: Configured security assessment agent
    """

    agent = LlmAgent(
        name="security_assessor",
        model="gemini-2.5-flash",
        description="Web security expert for domain safety assessment.",
        instruction="""You are a web security expert assistant. Your job is to help users
understand whether domains and websites are safe.

When assessing a domain, consider:
1. Well-known brands (google.com, microsoft.com, etc.) are legitimate
2. Typosquatting attempts (paypal-login.com, g00gle.com) are suspicious
3. Unusual TLDs combined with brand names may be phishing
4. Very short domains or random character sequences are suspicious
5. Domains mimicking official sites are likely malicious

Provide clear, concise safety assessments. Categorize domains as:
- SAFE: Well-known legitimate domains
- SUSPICIOUS: Potential typosquatting or unclear legitimacy
- DANGEROUS: Clear phishing or malicious attempts

Always explain your reasoning briefly."""
    )

    return agent


if __name__ == "__main__":
    # Test the agent interactively
    import asyncio
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types

    async def run_single_query(query, session_id):
        """Run a single query with a fresh agent instance."""
        agent = create_security_agent()
        session_service = InMemorySessionService()

        await session_service.create_session(
            app_name="security_test",
            user_id="test_user",
            session_id=session_id
        )

        runner = Runner(
            app_name="security_test",
            agent=agent,
            session_service=session_service
        )

        content = types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )

        events = runner.run_async(
            new_message=content,
            user_id="test_user",
            session_id=session_id
        )

        response = None
        async for event in events:
            if event.is_final_response():
                response = event.content.parts[0].text
                break

        # Allow cleanup to complete
        await asyncio.sleep(0.1)
        return response

    async def test_agent():
        test_queries = [
            "Is google.com safe?",
            "Is paypal-login.com safe?",
            "Is microsoft-support.xyz safe?"
        ]

        print("Testing Security Agent:\n")
        for i, query in enumerate(test_queries):
            response_text = await run_single_query(query, f"test_session_{i}")
            print(f"Q: {query}")
            print(f"A: {response_text}\n")

    asyncio.run(test_agent())
