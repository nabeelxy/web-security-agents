"""
Evaluation Runner

This script runs the security agent against the evaluation dataset and
collects results for analysis.
"""

import json
import time
from datetime import datetime
from pathlib import Path
import re
import asyncio
import warnings

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from security_agent import create_security_agent
from create_eval_dataset import load_eval_dataset

# Constants for session management
APP_NAME = "security_eval"
USER_ID = "eval_user"

# Suppress async client cleanup warnings
warnings.filterwarnings("ignore", category=ResourceWarning, message=".*unclosed.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)


def extract_verdict(response_text):
    """
    Extract the safety verdict from the agent's response.

    Looks for keywords: SAFE, SUSPICIOUS, DANGEROUS

    Args:
        response_text (str): Agent's response text

    Returns:
        str: Extracted verdict or "UNKNOWN" if not found
    """

    # Convert to uppercase for matching
    text_upper = response_text.upper()

    # Check for verdicts in order of specificity
    if "DANGEROUS" in text_upper or "MALICIOUS" in text_upper:
        return "DANGEROUS"
    elif "SUSPICIOUS" in text_upper or "QUESTIONABLE" in text_upper:
        return "SUSPICIOUS"
    elif "SAFE" in text_upper or "LEGITIMATE" in text_upper or "TRUSTED" in text_upper:
        return "SAFE"
    else:
        return "UNKNOWN"


async def run_single_eval(test_case, test_index):
    """
    Run a single evaluation test case.

    Args:
        test_case (dict): Test case with input and expected output
        test_index (int): Index for unique session ID

    Returns:
        dict: Evaluation result with actual vs expected
    """

    start_time = time.time()

    # Run the agent
    try:
        # Create unique session for this test
        session_id = f"eval_session_{test_index}"

        # Create fresh agent, session service, and runner for each test
        # This avoids async client lifecycle issues
        agent = create_security_agent()
        session_service = InMemorySessionService()

        # Create session
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )

        # Create runner
        runner = Runner(
            app_name=APP_NAME,
            agent=agent,
            session_service=session_service
        )

        # Format the query as ADK content
        content = types.Content(
            role="user",
            parts=[types.Part(text=test_case["input"])]
        )

        # Run the agent and collect response
        actual_response = ""
        events = runner.run_async(
            new_message=content,
            user_id=USER_ID,
            session_id=session_id,
        )

        async for event in events:
            if event.is_final_response():
                actual_response = event.content.parts[0].text
                break

        # Give a moment for cleanup to complete
        await asyncio.sleep(0.1)

        success = True
        error = None
    except Exception as e:
        actual_response = ""
        success = False
        error = str(e)

    end_time = time.time()
    latency = end_time - start_time

    # Extract verdict from response
    actual_verdict = extract_verdict(actual_response) if success else "ERROR"

    # Check if verdict matches expected
    expected_verdict = test_case["expected_verdict"]
    verdict_match = actual_verdict == expected_verdict

    # Build result
    result = {
        "test_id": test_case["id"],
        "category": test_case["category"],
        "input": test_case["input"],
        "expected_verdict": expected_verdict,
        "actual_verdict": actual_verdict,
        "actual_response": actual_response,
        "verdict_match": verdict_match,
        "success": success,
        "error": error,
        "latency_seconds": round(latency, 2)
    }

    return result


async def run_evaluation_async(dataset_path="eval_dataset.json", output_path="eval_results.json"):
    """
    Run the full evaluation suite (async).

    Args:
        dataset_path (str): Path to evaluation dataset
        output_path (str): Path to save results

    Returns:
        dict: Evaluation results with metrics
    """

    print("=" * 70)
    print("SECURITY AGENT EVALUATION")
    print("=" * 70)
    print()

    # Load dataset
    print(f"Loading dataset from: {dataset_path}")
    dataset = load_eval_dataset(dataset_path)
    test_cases = dataset["test_cases"]
    print(f"✓ Loaded {len(test_cases)} test cases\n")

    print("Running evaluations...")
    print("-" * 70)

    results = []
    correct = 0
    total = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{total}] {test_case['id']}: ", end="", flush=True)

        # Each test creates its own agent/runner to avoid async client issues
        result = await run_single_eval(test_case, i)
        results.append(result)

        # Print result
        if result["success"]:
            if result["verdict_match"]:
                print(f"✓ PASS ({result['actual_verdict']}) - {result['latency_seconds']}s")
                correct += 1
            else:
                print(f"✗ FAIL (expected {result['expected_verdict']}, got {result['actual_verdict']}) - {result['latency_seconds']}s")
        else:
            print(f"✗ ERROR: {result['error']}")

    print("-" * 70)
    print()

    # Calculate metrics
    accuracy = (correct / total * 100) if total > 0 else 0
    avg_latency = sum(r["latency_seconds"] for r in results) / len(results) if results else 0

    # Category breakdown
    category_stats = {}
    for result in results:
        cat = result["category"]
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "correct": 0}
        category_stats[cat]["total"] += 1
        if result["verdict_match"]:
            category_stats[cat]["correct"] += 1

    # Build final results
    eval_results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "dataset": dataset_path,
            "total_cases": total,
            "model": "gemini-2.0-flash"
        },
        "summary": {
            "total_tests": total,
            "passed": correct,
            "failed": total - correct,
            "accuracy_percent": round(accuracy, 2),
            "avg_latency_seconds": round(avg_latency, 2)
        },
        "category_breakdown": {
            cat: {
                "total": stats["total"],
                "correct": stats["correct"],
                "accuracy_percent": round(stats["correct"] / stats["total"] * 100, 2) if stats["total"] > 0 else 0
            }
            for cat, stats in category_stats.items()
        },
        "results": results
    }

    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(eval_results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total Tests:      {total}")
    print(f"Passed:           {correct}")
    print(f"Failed:           {total - correct}")
    print(f"Accuracy:         {accuracy:.2f}%")
    print(f"Avg Latency:      {avg_latency:.2f}s")
    print()

    print("CATEGORY BREAKDOWN")
    print("-" * 70)
    for cat, stats in eval_results["category_breakdown"].items():
        print(f"{cat:20} {stats['correct']:2}/{stats['total']:2} ({stats['accuracy_percent']:5.1f}%)")

    print()
    print(f"✓ Results saved to: {output_path}")
    print()

    return eval_results


def run_evaluation(dataset_path="eval_dataset.json", output_path="eval_results.json"):
    """
    Synchronous wrapper for run_evaluation_async.

    Args:
        dataset_path (str): Path to evaluation dataset
        output_path (str): Path to save results

    Returns:
        dict: Evaluation results with metrics
    """
    # Set up custom exception handler to suppress background task errors
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def exception_handler(loop, context):
        # Suppress BaseApiClient._async_httpx_client errors during cleanup
        exception = context.get('exception')
        if exception and isinstance(exception, AttributeError):
            if '_async_httpx_client' in str(exception):
                return  # Silently ignore this known cleanup issue
        # For other exceptions, use default handling
        loop.default_exception_handler(context)

    loop.set_exception_handler(exception_handler)

    try:
        result = loop.run_until_complete(run_evaluation_async(dataset_path, output_path))
        # Allow pending tasks to complete cleanup
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        return result
    finally:
        loop.close()


if __name__ == "__main__":
    # Run the evaluation
    results = run_evaluation()

    print("Next steps:")
    print("1. Review detailed results in: eval_results.json")
    print("2. Analyze failures with: python analyze_results.py")
    print("3. Improve agent and re-run evaluations")
