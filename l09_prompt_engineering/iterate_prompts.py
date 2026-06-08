"""
Prompt Iteration Workflow

Demonstrates how to debug and improve prompts through iteration.
Shows the evolution from a poor prompt to a production-ready one.
"""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.agents import LlmAgent


# Test case: Tricky domain that requires good analysis
TEST_DOMAIN = "microsoft-online.com"
TEST_EXPECTED_VERDICT = "SUSPICIOUS"
TEST_EXPECTED_REASONING = "Typosquatting microsoft.com (microsoft.com is real, but -online suffix is suspicious)"


async def test_prompt(prompt: str, iteration_number: int, domain: str):
    """Test a prompt and return the response."""
    agent = LlmAgent(
        name="test_agent",
        model="gemini-2.5-flash",
        description="Security analyst",
        instruction=prompt
    )

    session_service = InMemorySessionService()
    session_id = f"iteration_{iteration_number}"

    await session_service.create_session(
        app_name="prompt_iteration",
        user_id="dev",
        session_id=session_id
    )

    runner = Runner(
        app_name="prompt_iteration",
        agent=agent,
        session_service=session_service
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=f"Analyze this domain: {domain}")]
    )

    events = runner.run_async(
        new_message=content,
        user_id="dev",
        session_id=session_id
    )

    async for event in events:
        if event.is_final_response():
            response = event.content.parts[0].text
            await asyncio.sleep(0.1)
            return response

    return "No response"


def extract_verdict(response: str) -> str:
    """Extract the verdict from response."""
    text_upper = response.upper()
    if "DANGEROUS" in text_upper:
        return "DANGEROUS"
    elif "SUSPICIOUS" in text_upper:
        return "SUSPICIOUS"
    elif "SAFE" in text_upper:
        return "SAFE"
    else:
        return "UNKNOWN"


def evaluate_response(response: str, expected_verdict: str) -> dict:
    """Evaluate if response meets quality criteria."""
    issues = []

    # Extract actual verdict
    actual_verdict = extract_verdict(response)

    # Check if verdict is present
    if actual_verdict == "UNKNOWN":
        issues.append("❌ No clear verdict (SAFE/SUSPICIOUS/DANGEROUS)")

    # Check if expected verdict matches
    if actual_verdict != expected_verdict:
        issues.append(f"❌ Expected '{expected_verdict}' but got '{actual_verdict}'")

    # Check for reasoning
    if len(response) < 50:
        issues.append("❌ Response too short, lacks reasoning")

    # Check for structure
    if response.count('\n') < 2:
        issues.append("⚠️  Response lacks structure (no line breaks)")

    # Check for specificity
    generic_words = ["might", "could be", "possibly", "maybe"]
    if any(word in response.lower() for word in generic_words):
        issues.append("⚠️  Uses uncertain language")

    return {
        "passed": len([i for i in issues if i.startswith("❌")]) == 0,
        "actual_verdict": actual_verdict,
        "expected_verdict": expected_verdict,
        "issues": issues
    }


async def iteration_1():
    """Iteration 1: Minimal prompt (baseline)."""
    print("=" * 70)
    print("ITERATION 1: BASELINE (Minimal Prompt)")
    print("=" * 70)

    prompt = """You are a security expert."""

    print("\nPrompt:")
    print(prompt)
    print(f"\nTest Domain: {TEST_DOMAIN}")
    print("\nResponse:")

    response = await test_prompt(prompt, 1, TEST_DOMAIN)
    print(response)

    print("\n" + "-" * 70)
    print("VERDICT EVALUATION:")
    print("-" * 70)

    eval_result = evaluate_response(response, TEST_EXPECTED_VERDICT)

    # Show verdict comparison
    actual = eval_result["actual_verdict"]
    expected = eval_result["expected_verdict"]
    verdict_match = actual == expected

    if verdict_match:
        print(f"✅ VERDICT: {actual} (Correct!)")
    else:
        print(f"❌ VERDICT: {actual} (Expected: {expected})")

    print("\nQuality Issues:")
    for issue in eval_result["issues"]:
        print(f"  {issue}")

    if not eval_result["passed"]:
        print("\n💡 PROBLEM: Vague prompt leads to inconsistent, unstructured output")
        print("🔧 FIX: Add clear role, task definition, and output format")

    return eval_result


async def iteration_2():
    """Iteration 2: Add structure."""
    print("\n\n" + "=" * 70)
    print("ITERATION 2: ADD STRUCTURE")
    print("=" * 70)

    prompt = """You are a security expert specializing in domain analysis.

        Analyze domains and provide:
        1. Risk Level (SAFE/SUSPICIOUS/DANGEROUS)
        2. Reasoning
        3. Recommendation"""

    print("\nPrompt:")
    print(prompt)
    print(f"\nTest Domain: {TEST_DOMAIN}")
    print("\nResponse:")

    response = await test_prompt(prompt, 2, TEST_DOMAIN)
    print(response)

    print("\n" + "-" * 70)
    print("VERDICT EVALUATION:")
    print("-" * 70)

    eval_result = evaluate_response(response, TEST_EXPECTED_VERDICT)

    actual = eval_result["actual_verdict"]
    expected = eval_result["expected_verdict"]
    verdict_match = actual == expected

    if verdict_match:
        print(f"✅ VERDICT: {actual} (Correct!)")
    else:
        print(f"❌ VERDICT: {actual} (Expected: {expected})")

    print("\nQuality Issues:")
    if eval_result["issues"]:
        for issue in eval_result["issues"]:
            print(f"  {issue}")
    else:
        print("  ✅ No issues found")

    if not eval_result["passed"]:
        print("\n💡 PROBLEM: Structure is better but lacks specific criteria")
        print("🔧 FIX: Add methodology and examples")

    return eval_result


async def iteration_3():
    """Iteration 3: Add methodology."""
    print("\n\n" + "=" * 70)
    print("ITERATION 3: ADD METHODOLOGY")
    print("=" * 70)

    prompt = """You are a security expert specializing in domain analysis.

        ANALYSIS CRITERIA:
        - Character substitutions (0 for o, 1 for l) indicate typosquatting
        - Suspicious keywords (verify, login, secure, account) suggest phishing
        - Uncommon TLDs (.xyz, .tk, .ml) are higher risk
        - Extra hyphens or subdomains may indicate impersonation

        OUTPUT FORMAT:
        1. Risk Level: [SAFE/SUSPICIOUS/DANGEROUS]
        2. Key Indicators: [Specific findings]
        3. Recommendation: [What to do]"""

    print("\nPrompt:")
    print(prompt)
    print(f"\nTest Domain: {TEST_DOMAIN}")
    print("\nResponse:")

    response = await test_prompt(prompt, 3, TEST_DOMAIN)
    print(response)

    print("\n" + "-" * 70)
    print("VERDICT EVALUATION:")
    print("-" * 70)

    eval_result = evaluate_response(response, TEST_EXPECTED_VERDICT)

    actual = eval_result["actual_verdict"]
    expected = eval_result["expected_verdict"]
    verdict_match = actual == expected

    if verdict_match:
        print(f"✅ VERDICT: {actual} (Correct!)")
    else:
        print(f"❌ VERDICT: {actual} (Expected: {expected})")

    print("\nQuality Issues:")
    if eval_result["issues"]:
        for issue in eval_result["issues"]:
            print(f"  {issue}")
    else:
        print("  ✅ No issues found")

    if not eval_result["passed"]:
        print("\n💡 PROBLEM: Methodology helps but agent needs examples")
        print("🔧 FIX: Add few-shot examples")

    return eval_result


async def iteration_4():
    """Iteration 4: Add few-shot examples."""
    print("\n\n" + "=" * 70)
    print("ITERATION 4: ADD FEW-SHOT EXAMPLES")
    print("=" * 70)

    prompt = """You are a security expert specializing in domain analysis.

    ANALYSIS CRITERIA:
    - Character substitutions (0 for o, 1 for l) indicate typosquatting
    - Suspicious keywords (verify, login, secure, account) suggest phishing
    - Uncommon TLDs (.xyz, .tk, .ml) are higher risk
    - Extra hyphens or subdomains may indicate impersonation

    EXAMPLES:

    Domain: paypal.com
    Risk Level: SAFE
    Key Indicators: Official PayPal domain, .com TLD, no suspicious patterns
    Recommendation: This is the legitimate PayPal website

    Domain: paypa1-verify.xyz
    Risk Level: DANGEROUS
    Key Indicators: Character substitution (1→l), "verify" keyword, .xyz TLD
    Recommendation: Phishing attempt. Do not visit.

    Domain: amazon-deals.com
    Risk Level: SAFE
    Key Indicators: Belongs to Amazon even though it is not the official site.
    Recommendation: This is a legimate site defensively registered by Amazon.

    Domain: google-deals.com
    Risk Level: SUSPICIOUS
    Key Indicators: Does not own by Google and some security vendors have flaged it as phishing.
    Recommendation: Likely phishing attempt. Do not visit.

    OUTPUT FORMAT:
    Risk Level: [SAFE/SUSPICIOUS/DANGEROUS]
    Key Indicators: [Specific findings]
    Recommendation: [What to do]"""

    print("\nPrompt:")
    print(prompt[:200] + "... [abbreviated]")
    print(f"\nTest Domain: {TEST_DOMAIN}")
    print("\nResponse:")

    response = await test_prompt(prompt, 4, TEST_DOMAIN)
    print(response)

    print("\n" + "-" * 70)
    print("VERDICT EVALUATION:")
    print("-" * 70)

    eval_result = evaluate_response(response, TEST_EXPECTED_VERDICT)

    actual = eval_result["actual_verdict"]
    expected = eval_result["expected_verdict"]
    verdict_match = actual == expected

    if verdict_match:
        print(f"✅ VERDICT: {actual} (Correct!)")
    else:
        print(f"❌ VERDICT: {actual} (Expected: {expected})")

    print("\nQuality Issues:")
    if eval_result["issues"]:
        for issue in eval_result["issues"]:
            print(f"  {issue}")
    else:
        print("  ✅ No issues found")

    if eval_result["passed"]:
        print("\n✨ SUCCESS: Prompt now produces consistent, high-quality outputs")
        print("📊 Ready for production use")

    return eval_result


async def run_all_iterations():
    """Run all iterations and show summary."""
    print("\n")
    print("*" * 70)
    print("PROMPT ITERATION WORKFLOW - ALL ITERATIONS")
    print("*" * 70)
    print("\nDemonstrates the process of debugging and improving prompts")
    print(f"Test Domain: {TEST_DOMAIN}")
    print(f"Expected Verdict: {TEST_EXPECTED_VERDICT}")
    print(f"Expected Reasoning: {TEST_EXPECTED_REASONING}\n")

    # Run all iterations
    results = []

    result_1 = await iteration_1()
    results.append(("Iteration 1: Minimal", result_1))

    result_2 = await iteration_2()
    results.append(("Iteration 2: + Structure", result_2))

    result_3 = await iteration_3()
    results.append(("Iteration 3: + Methodology", result_3))

    result_4 = await iteration_4()
    results.append(("Iteration 4: + Examples", result_4))

    # Summary table
    print("\n\n" + "*" * 70)
    print("ITERATION SUMMARY TABLE")
    print("*" * 70)
    print()
    print(f"{'Iteration':<30} {'Verdict':<15} {'Correct?':<10} {'Quality':<10}")
    print("-" * 70)

    for name, result in results:
        actual = result["actual_verdict"]
        expected = result["expected_verdict"]
        correct = "✅ Yes" if actual == expected else "❌ No"
        quality = "✅ Pass" if result["passed"] else "❌ Fail"
        print(f"{name:<30} {actual:<15} {correct:<10} {quality:<10}")

    print("-" * 70)

    # Key lessons
    print("\n" + "*" * 70)
    print("KEY LESSONS")
    print("*" * 70)
    print("""
1. Start minimal, iterate based on failures
   → Iteration 1 shows what happens with vague prompts

2. Add structure before adding complexity
   → Iteration 2 improves format consistency

3. Methodology guides reasoning
   → Iteration 3 provides explicit criteria

4. Examples teach desired behavior
   → Iteration 4 shows the complete pattern

5. Test with tricky cases, not just easy ones
   → {domain} is intentionally ambiguous

Evolution:
  Minimal → Inconsistent outputs
  + Structure → Better format
  + Methodology → Clear criteria
  + Examples → Production-ready ✅
    """.format(domain=TEST_DOMAIN))


async def run_single_iteration(iteration_num: int):
    """Run a single iteration."""
    iterations = {
        1: iteration_1,
        2: iteration_2,
        3: iteration_3,
        4: iteration_4
    }

    if iteration_num not in iterations:
        print(f"Error: Invalid iteration number {iteration_num}")
        print("Valid options: 1, 2, 3, 4")
        return

    print(f"\nRunning Iteration {iteration_num} only...\n")
    result = await iterations[iteration_num]()

    # Show final verdict
    print("\n" + "*" * 70)
    print(f"ITERATION {iteration_num} FINAL RESULT")
    print("*" * 70)
    actual = result["actual_verdict"]
    expected = result["expected_verdict"]

    print(f"\nDomain: {TEST_DOMAIN}")
    print(f"Actual Verdict: {actual}")
    print(f"Expected Verdict: {expected}")
    print(f"Match: {'✅ YES' if actual == expected else '❌ NO'}")
    print(f"Quality Check: {'✅ PASS' if result['passed'] else '❌ FAIL'}")


if __name__ == "__main__":
    import sys

    print("\n⚠️  NOTE: This script makes LLM API calls")

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python iterate_prompts.py --run           # Run all iterations")
        print("  python iterate_prompts.py --iteration 1   # Run iteration 1 only")
        print("  python iterate_prompts.py --iteration 2   # Run iteration 2 only")
        print("  python iterate_prompts.py --iteration 3   # Run iteration 3 only")
        print("  python iterate_prompts.py --iteration 4   # Run iteration 4 only")
        print()
    elif sys.argv[1] == "--run":
        asyncio.run(run_all_iterations())
    elif sys.argv[1] == "--iteration" and len(sys.argv) > 2:
        try:
            iteration_num = int(sys.argv[2])
            asyncio.run(run_single_iteration(iteration_num))
        except ValueError:
            print(f"Error: '{sys.argv[2]}' is not a valid iteration number")
            print("Use: 1, 2, 3, or 4")
    else:
        print("Invalid arguments. Use --run or --iteration <num>")
