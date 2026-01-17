"""
Evaluation Results Analyzer

This script provides detailed analysis of evaluation results,
helping identify patterns in failures and areas for improvement.
"""

import json
from pathlib import Path
from collections import defaultdict


def load_results(results_path="eval_results.json"):
    """Load evaluation results from file."""
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_failures(results):
    """
    Analyze failed test cases to identify patterns.

    Args:
        results (dict): Evaluation results

    Returns:
        dict: Analysis of failures
    """

    failures = [r for r in results["results"] if not r["verdict_match"]]

    if not failures:
        print("🎉 No failures! All tests passed.")
        return {}

    print("FAILURE ANALYSIS")
    print("=" * 70)
    print(f"Total Failures: {len(failures)}\n")

    # Group by error type
    error_patterns = defaultdict(list)

    for failure in failures:
        expected = failure["expected_verdict"]
        actual = failure["actual_verdict"]
        error_type = f"{expected} → {actual}"
        error_patterns[error_type].append(failure)

    # Display by error pattern
    print("ERROR PATTERNS")
    print("-" * 70)
    for error_type, cases in sorted(error_patterns.items(), key=lambda x: -len(x[1])):
        print(f"\n{error_type} ({len(cases)} cases):")
        for case in cases:
            print(f"  • {case['test_id']}: {case['input']}")
            if case.get('error'):
                print(f"    Error: {case['error']}")
            else:
                # Show first 100 chars of response
                response_preview = case['actual_response'][:100].replace('\n', ' ')
                print(f"    Response: {response_preview}...")

    print()

    # Category performance
    print("\nCATEGORY-SPECIFIC FAILURES")
    print("-" * 70)

    category_failures = defaultdict(list)
    for failure in failures:
        category_failures[failure["category"]].append(failure)

    for category, cases in sorted(category_failures.items()):
        print(f"\n{category} ({len(cases)} failures):")
        for case in cases:
            print(f"  • {case['test_id']}: Expected {case['expected_verdict']}, got {case['actual_verdict']}")

    return {
        "total_failures": len(failures),
        "error_patterns": {k: len(v) for k, v in error_patterns.items()},
        "category_failures": {k: len(v) for k, v in category_failures.items()}
    }


def compare_results(results1_path, results2_path):
    """
    Compare two evaluation runs to see improvements or regressions.

    Args:
        results1_path (str): Path to first results file
        results2_path (str): Path to second results file
    """

    print("\nRESULTS COMPARISON")
    print("=" * 70)

    r1 = load_results(results1_path)
    r2 = load_results(results2_path)

    # Overall metrics
    print(f"Run 1: {r1['metadata']['timestamp']}")
    print(f"  Accuracy: {r1['summary']['accuracy_percent']}%")
    print(f"  Avg Latency: {r1['summary']['avg_latency_seconds']}s")

    print(f"\nRun 2: {r2['metadata']['timestamp']}")
    print(f"  Accuracy: {r2['summary']['accuracy_percent']}%")
    print(f"  Avg Latency: {r2['summary']['avg_latency_seconds']}s")

    # Calculate changes
    acc_change = r2['summary']['accuracy_percent'] - r1['summary']['accuracy_percent']
    latency_change = r2['summary']['avg_latency_seconds'] - r1['summary']['avg_latency_seconds']

    print(f"\nChanges:")
    print(f"  Accuracy: {acc_change:+.2f}%")
    print(f"  Latency: {latency_change:+.2f}s")

    # Per-category changes
    print("\nCategory Changes:")
    for cat in r1['category_breakdown']:
        if cat in r2['category_breakdown']:
            acc1 = r1['category_breakdown'][cat]['accuracy_percent']
            acc2 = r2['category_breakdown'][cat]['accuracy_percent']
            change = acc2 - acc1
            print(f"  {cat:20} {change:+.2f}%")


def generate_report(results_path="eval_results.json", output_path="eval_report.txt"):
    """
    Generate a human-readable evaluation report.

    Args:
        results_path (str): Path to results JSON
        output_path (str): Path to save report
    """

    results = load_results(results_path)

    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("SECURITY AGENT EVALUATION REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"Generated: {results['metadata']['timestamp']}")
    report_lines.append(f"Model: {results['metadata']['model']}")
    report_lines.append(f"Dataset: {results['metadata']['dataset']}")
    report_lines.append("")

    # Summary
    summary = results['summary']
    report_lines.append("OVERALL PERFORMANCE")
    report_lines.append("-" * 70)
    report_lines.append(f"Total Tests:       {summary['total_tests']}")
    report_lines.append(f"Passed:            {summary['passed']}")
    report_lines.append(f"Failed:            {summary['failed']}")
    report_lines.append(f"Accuracy:          {summary['accuracy_percent']}%")
    report_lines.append(f"Avg Latency:       {summary['avg_latency_seconds']}s")
    report_lines.append("")

    # Category breakdown
    report_lines.append("CATEGORY BREAKDOWN")
    report_lines.append("-" * 70)
    for cat, stats in results['category_breakdown'].items():
        report_lines.append(f"{cat:25} {stats['correct']}/{stats['total']} ({stats['accuracy_percent']}%)")
    report_lines.append("")

    # Failed cases
    failures = [r for r in results["results"] if not r["verdict_match"]]
    if failures:
        report_lines.append("FAILED TEST CASES")
        report_lines.append("-" * 70)
        for f in failures:
            report_lines.append(f"\nID: {f['test_id']}")
            report_lines.append(f"Category: {f['category']}")
            report_lines.append(f"Input: {f['input']}")
            report_lines.append(f"Expected: {f['expected_verdict']}")
            report_lines.append(f"Actual: {f['actual_verdict']}")
            report_lines.append(f"Response: {f['actual_response'][:200]}...")
        report_lines.append("")

    # Recommendations
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 70)

    accuracy = summary['accuracy_percent']
    if accuracy >= 95:
        report_lines.append("✓ Excellent performance! Agent is production-ready.")
    elif accuracy >= 85:
        report_lines.append("• Good performance. Review failures for edge case improvements.")
    elif accuracy >= 70:
        report_lines.append("• Moderate performance. Significant improvements needed.")
    else:
        report_lines.append("• Poor performance. Major agent redesign recommended.")

    # Category-specific recommendations
    for cat, stats in results['category_breakdown'].items():
        if stats['accuracy_percent'] < 80:
            report_lines.append(f"• {cat}: Low accuracy ({stats['accuracy_percent']}%) - needs attention")

    report_lines.append("")
    report_lines.append("=" * 70)

    # Save report
    report_text = "\n".join(report_lines)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    # Print to console
    print(report_text)
    print(f"\n✓ Report saved to: {output_path}")


def main():
    """Main analysis function."""

    print("EVALUATION RESULTS ANALYZER")
    print("=" * 70)
    print()

    # Check if results exist
    results_path = "eval_results.json"
    if not Path(results_path).exists():
        print(f"❌ Results file not found: {results_path}")
        print("Run 'python run_eval.py' first to generate results.")
        return

    # Load and display summary
    results = load_results(results_path)
    print(f"Loaded results from: {results['metadata']['timestamp']}")
    print(f"Accuracy: {results['summary']['accuracy_percent']}%")
    print()

    # Analyze failures
    analyze_failures(results)

    # Generate detailed report
    print("\n" + "=" * 70)
    generate_report(results_path)

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
