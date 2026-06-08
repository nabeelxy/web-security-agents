"""
Compare Different Prompting Strategies

This script demonstrates the impact of prompt engineering by running
the same domain through different prompting approaches.
"""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.agents import LlmAgent

from prompts import (
    BASIC_SYSTEM_PROMPT,
    OPTIMIZED_SYSTEM_PROMPT,
    FEW_SHOT_PROMPT,
    CHAIN_OF_THOUGHT_PROMPT,
    PRODUCTION_PROMPT,
    STRUCTURED_OUTPUT_PROMPT,
    GROUNDED_PROMPT,
)


async def run_agent_with_prompt(system_prompt: str, user_prompt: str, session_id: str):
    """
    Run agent with a specific prompt configuration.

    Args:
        system_prompt: System-level instructions
        user_prompt: User query
        session_id: Unique session identifier

    Returns:
        Agent's response text
    """
    # Create agent with given system prompt
    agent = LlmAgent(
        name="prompt_test_agent",
        model="gemini-2.5-flash",
        description="Security domain analyst",
        instruction=system_prompt
    )

    # Setup session
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="prompt_comparison",
        user_id="test_user",
        session_id=session_id
    )

    # Create runner
    runner = Runner(
        app_name="prompt_comparison",
        agent=agent,
        session_service=session_service
    )

    # Run query
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_prompt)]
    )

    events = runner.run_async(
        new_message=content,
        user_id="test_user",
        session_id=session_id
    )

    # Get response
    async for event in events:
        if event.is_final_response():
            response = event.content.parts[0].text
            await asyncio.sleep(0.1)  # Cleanup
            return response

    return "No response"


async def compare_basic_vs_optimized():
    """Compare basic vs optimized system prompts."""
    test_domain = "paypa1-verify.com"
    user_query = f"Is {test_domain} safe?"

    print("=" * 70)
    print("COMPARISON 1: BASIC vs OPTIMIZED SYSTEM PROMPT")
    print("=" * 70)
    print(f"\nTest Domain: {test_domain}")
    print(f"User Query: {user_query}\n")

    # Basic prompt
    print("─" * 70)
    print("BASIC SYSTEM PROMPT:")
    print("─" * 70)
    print(BASIC_SYSTEM_PROMPT)
    print("\nResponse:")
    basic_response = await run_agent_with_prompt(
        BASIC_SYSTEM_PROMPT,
        user_query,
        "basic_session"
    )
    print(basic_response)

    print("\n")

    # Optimized prompt
    print("─" * 70)
    print("OPTIMIZED SYSTEM PROMPT:")
    print("─" * 70)
    print(OPTIMIZED_SYSTEM_PROMPT[:200] + "...")
    print("\nResponse:")
    optimized_response = await run_agent_with_prompt(
        OPTIMIZED_SYSTEM_PROMPT,
        user_query,
        "optimized_session"
    )
    print(optimized_response)

    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS:")
    print("=" * 70)
    print("✓ Optimized prompt provides:")
    print("  - Clear risk categorization")
    print("  - Structured format")
    print("  - Specific indicators")
    print("  - Actionable recommendations")
    print("\n✗ Basic prompt typically results in:")
    print("  - Inconsistent format")
    print("  - Vague or incomplete analysis")
    print("  - Missing actionable guidance")


async def demonstrate_few_shot():
    """Demonstrate few-shot learning effectiveness."""
    test_domain = "g00gle-support.xyz"

    print("\n\n" + "=" * 70)
    print("COMPARISON 2: FEW-SHOT LEARNING")
    print("=" * 70)
    print(f"\nTest Domain: {test_domain}\n")

    # Create prompt with domain
    few_shot_query = FEW_SHOT_PROMPT + f"\nDomain: {test_domain}"

    print("─" * 70)
    print("FEW-SHOT PROMPT (with 3 examples):")
    print("─" * 70)
    print("Shows examples of SAFE, DANGEROUS, and SUSPICIOUS domains")
    print("with desired output format\n")

    print("Response:")
    response = await run_agent_with_prompt(
        "You are a security expert.",
        few_shot_query,
        "fewshot_session"
    )
    print(response)

    print("\n" + "=" * 70)
    print("ANALYSIS:")
    print("=" * 70)
    print("✓ Few-shot learning teaches:")
    print("  - Exact output format to follow")
    print("  - Reasoning patterns to apply")
    print("  - Consistency across responses")


async def demonstrate_chain_of_thought():
    """Demonstrate chain-of-thought prompting."""
    test_domain = "amaz0n-login.secure-verify.com"

    print("\n\n" + "=" * 70)
    print("COMPARISON 3: CHAIN-OF-THOUGHT REASONING")
    print("=" * 70)
    print(f"\nTest Domain: {test_domain}\n")

    # CoT query
    cot_query = CHAIN_OF_THOUGHT_PROMPT + f"\nDomain: {test_domain}"

    print("─" * 70)
    print("CHAIN-OF-THOUGHT PROMPT:")
    print("─" * 70)
    print("Guides agent through step-by-step analysis\n")

    print("Response:")
    response = await run_agent_with_prompt(
        "You are a security analyst.",
        cot_query,
        "cot_session"
    )
    print(response)

    print("\n" + "=" * 70)
    print("ANALYSIS:")
    print("=" * 70)
    print("✓ Chain-of-thought prompting:")
    print("  - Breaks down complex reasoning")
    print("  - Shows working/logic")
    print("  - Reduces errors through structured thinking")
    print("  - Makes debugging easier (can see where logic fails)")


async def demonstrate_structured_output():
    """Demonstrate structured output format enforcement."""
    test_domain = "microsoft-security-update.tk"

    print("\n\n" + "=" * 70)
    print("COMPARISON 4: STRUCTURED OUTPUT FORMAT")
    print("=" * 70)
    print(f"\nTest Domain: {test_domain}\n")

    query = STRUCTURED_OUTPUT_PROMPT + f"\n{test_domain}"

    print("─" * 70)
    print("STRUCTURED OUTPUT PROMPT:")
    print("─" * 70)
    print(STRUCTURED_OUTPUT_PROMPT)

    print("\nResponse:")
    response = await run_agent_with_prompt(
        "You are a security expert.",
        query,
        "structured_session"
    )
    print(response)

    print("\n" + "=" * 70)
    print("ANALYSIS:")
    print("=" * 70)
    print("✓ Structured format ensures:")
    print("  - Parseable output (can extract programmatically)")
    print("  - Consistent field presence")
    print("  - Easier downstream processing")
    print("  - Clear separation of verdict/reasoning/action")


async def demonstrate_production_prompt():
    """Demonstrate production-grade prompt combining all techniques."""
    test_domain = "paypal-secure.account-verify.xyz"

    print("\n\n" + "=" * 70)
    print("COMPARISON 5: PRODUCTION PROMPT (ALL TECHNIQUES COMBINED)")
    print("=" * 70)
    print(f"\nTest Domain: {test_domain}\n")

    query = f"Domain: {test_domain}"

    print("─" * 70)
    print("PRODUCTION PROMPT:")
    print("─" * 70)
    print("Combines: System instructions + Methodology + Examples + Structure")
    print(f"(See prompts.py for full prompt - {len(PRODUCTION_PROMPT)} chars)\n")

    print("Response:")
    response = await run_agent_with_prompt(
        PRODUCTION_PROMPT,
        query,
        "production_session"
    )
    print(response)

    print("\n" + "=" * 70)
    print("ANALYSIS:")
    print("=" * 70)
    print("✓ Production prompt includes:")
    print("  - Clear role and methodology (system)")
    print("  - Step-by-step process (CoT)")
    print("  - Example outputs (few-shot)")
    print("  - Structured format (parseable)")
    print("  - Explicit constraints (reduces hallucination)")


async def main():
    """Run all comparisons."""
    print("\n")
    print("*" * 70)
    print("PROMPT ENGINEERING COMPARISON SUITE")
    print("*" * 70)
    print("\nThis demo shows how different prompting strategies affect")
    print("agent behavior on the same security analysis task.\n")

    await compare_basic_vs_optimized()
    await demonstrate_few_shot()
    await demonstrate_chain_of_thought()
    await demonstrate_structured_output()
    await demonstrate_production_prompt()

    print("\n\n" + "*" * 70)
    print("KEY TAKEAWAYS")
    print("*" * 70)
    print("""
1. SYSTEM PROMPTS: Be specific about role, format, and constraints
2. FEW-SHOT: Show examples of desired behavior
3. CHAIN-OF-THOUGHT: Guide step-by-step reasoning for complex tasks
4. STRUCTURED OUTPUT: Define exact format for parseable responses
5. COMBINE TECHNIQUES: Production prompts use all of the above

Remember: Time spent on prompt engineering > time spent debugging bad outputs
""")


if __name__ == "__main__":
    print("\n⚠️  NOTE: This script makes multiple LLM API calls")
    print("Expected runtime: 1-2 minutes")
    print("Cost: ~$0.01-0.05 depending on model pricing\n")

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        asyncio.run(main())
    else:
        print("To run the comparison, use: python compare_prompts.py --run")
        print("\nOr explore individual techniques in prompts.py")
