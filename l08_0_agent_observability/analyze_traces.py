"""
Trace Analysis Tool

Analyzes trace files to provide insights into agent performance:
- Aggregate statistics across multiple traces
- Identify slow operations
- Tool usage patterns
- Error analysis
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict


def load_trace(filepath: str) -> Dict[str, Any]:
    """Load a single trace file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_all_traces(traces_dir: str = "traces") -> List[Dict[str, Any]]:
    """Load all trace files from directory."""
    traces = []
    trace_path = Path(traces_dir)

    if not trace_path.exists():
        print(f"No traces directory found at: {traces_dir}")
        return traces

    for filepath in trace_path.glob("trace_*.json"):
        try:
            trace = load_trace(str(filepath))
            traces.append(trace)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    return traces


def analyze_traces(traces: List[Dict[str, Any]]):
    """Analyze multiple traces and print insights."""

    if not traces:
        print("No traces to analyze")
        return

    print("=" * 70)
    print("TRACE ANALYSIS")
    print("=" * 70)

    # Overall stats
    print(f"\n📊 Overall Statistics:")
    print(f"  Total traces: {len(traces)}")

    total_duration = sum(t.get('total_duration_ms', 0) for t in traces)
    avg_duration = total_duration / len(traces) if traces else 0
    print(f"  Total execution time: {total_duration:.2f}ms")
    print(f"  Average execution time: {avg_duration:.2f}ms")

    # Success/failure rates
    successful = sum(1 for t in traces if t.get('summary', {}).get('error_spans', 0) == 0)
    print(f"  Successful: {successful}/{len(traces)} ({successful/len(traces)*100:.1f}%)")

    # Span analysis
    print(f"\n🔍 Span Analysis:")
    span_stats = defaultdict(lambda: {"count": 0, "total_duration": 0, "errors": 0})

    for trace in traces:
        for span in trace.get('spans', []):
            name = span['name']
            span_stats[name]['count'] += 1
            span_stats[name]['total_duration'] += span.get('duration_ms', 0)
            if span.get('status') == 'error':
                span_stats[name]['errors'] += 1

    print(f"\n  Span Type Breakdown:")
    for span_name, stats in sorted(span_stats.items(), key=lambda x: x[1]['total_duration'], reverse=True):
        avg_dur = stats['total_duration'] / stats['count'] if stats['count'] > 0 else 0
        error_rate = stats['errors'] / stats['count'] * 100 if stats['count'] > 0 else 0
        print(f"    {span_name}:")
        print(f"      Count: {stats['count']}")
        print(f"      Avg Duration: {avg_dur:.2f}ms")
        print(f"      Total Duration: {stats['total_duration']:.2f}ms")
        if stats['errors'] > 0:
            print(f"      Error Rate: {error_rate:.1f}% ({stats['errors']}/{stats['count']})")

    # Tool usage analysis
    print(f"\n🔧 Tool Usage:")
    tool_calls = []
    for trace in traces:
        for span in trace.get('spans', []):
            if span['name'] == 'tool_call':
                tool_name = span.get('attributes', {}).get('tool_name', 'unknown')
                tool_calls.append({
                    'name': tool_name,
                    'duration': span.get('duration_ms', 0),
                    'status': span.get('status', 'unknown')
                })

    if tool_calls:
        tool_stats = defaultdict(lambda: {"count": 0, "total_duration": 0})
        for call in tool_calls:
            tool_stats[call['name']]['count'] += 1
            tool_stats[call['name']]['total_duration'] += call['duration']

        for tool_name, stats in tool_stats.items():
            avg = stats['total_duration'] / stats['count'] if stats['count'] > 0 else 0
            print(f"  {tool_name}:")
            print(f"    Invocations: {stats['count']}")
            print(f"    Avg Duration: {avg:.2f}ms")
    else:
        print("  No tool calls recorded")

    # Performance insights
    print(f"\n⚡ Performance Insights:")

    # Find slowest traces
    slowest = sorted(traces, key=lambda t: t.get('total_duration_ms', 0), reverse=True)[:3]
    print(f"\n  Slowest Traces:")
    for i, trace in enumerate(slowest, 1):
        print(f"    {i}. {trace['trace_id']}: {trace.get('total_duration_ms', 0):.2f}ms")
        # Find slowest span in this trace
        if trace.get('spans'):
            slowest_span = max(trace['spans'], key=lambda s: s.get('duration_ms', 0))
            print(f"       Bottleneck: {slowest_span['name']} ({slowest_span.get('duration_ms', 0):.2f}ms)")

    # Find fastest traces
    fastest = sorted(traces, key=lambda t: t.get('total_duration_ms', 0))[:3]
    print(f"\n  Fastest Traces:")
    for i, trace in enumerate(fastest, 1):
        print(f"    {i}. {trace['trace_id']}: {trace.get('total_duration_ms', 0):.2f}ms")

    print("\n" + "=" * 70)


def compare_traces(trace_ids: List[str], traces_dir: str = "traces"):
    """Compare specific traces side-by-side."""
    print("=" * 70)
    print("TRACE COMPARISON")
    print("=" * 70)

    traces_to_compare = []
    for trace_id in trace_ids:
        filepath = Path(traces_dir) / f"{trace_id}.json"
        if filepath.exists():
            traces_to_compare.append(load_trace(str(filepath)))
        else:
            print(f"Warning: Trace {trace_id} not found")

    if len(traces_to_compare) < 2:
        print("Need at least 2 traces to compare")
        return

    print(f"\nComparing {len(traces_to_compare)} traces:\n")

    # Compare durations
    print("Duration Comparison:")
    for trace in traces_to_compare:
        print(f"  {trace['trace_id']}: {trace.get('total_duration_ms', 0):.2f}ms")

    # Compare span counts
    print(f"\nSpan Count Comparison:")
    for trace in traces_to_compare:
        print(f"  {trace['trace_id']}: {len(trace.get('spans', []))} spans")

    # Compare tool calls
    print(f"\nTool Call Comparison:")
    for trace in traces_to_compare:
        tool_spans = [s for s in trace.get('spans', []) if s['name'] == 'tool_call']
        print(f"  {trace['trace_id']}: {len(tool_spans)} tool calls")

    print("\n" + "=" * 70)


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        # Compare specific traces
        trace_ids = sys.argv[1:]
        compare_traces(trace_ids)
    else:
        # Analyze all traces
        traces = load_all_traces("traces")
        analyze_traces(traces)


if __name__ == "__main__":
    main()
