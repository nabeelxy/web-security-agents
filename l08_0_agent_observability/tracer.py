"""
Simple Observability and Tracing Module

This module provides basic tracing capabilities for monitoring agent behavior:
- Tool invocations and their results
- LLM API calls and token usage
- Execution timing
- Error tracking

Demonstrates core observability concepts without requiring external services.
"""

import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict, field
from contextlib import contextmanager


@dataclass
class Span:
    """
    Represents a single traced operation (like an HTTP span).

    Attributes:
        span_id: Unique identifier for this span
        parent_id: ID of parent span (for nested operations)
        name: Human-readable operation name
        start_time: When operation started
        end_time: When operation completed
        duration_ms: How long operation took
        attributes: Key-value metadata about the operation
        status: Operation status (success/error)
        error: Error message if failed
    """
    span_id: str
    name: str
    start_time: float
    parent_id: Optional[str] = None
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    status: str = "in_progress"
    error: Optional[str] = None

    def finish(self, status: str = "success", error: Optional[str] = None):
        """Mark span as complete and calculate duration."""
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)
        self.status = status
        self.error = error


@dataclass
class Trace:
    """
    Represents a complete trace of an agent invocation.

    A trace contains multiple spans representing different operations.
    """
    trace_id: str
    spans: List[Span] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    total_duration_ms: Optional[float] = None

    def add_span(self, span: Span):
        """Add a span to this trace."""
        self.spans.append(span)

    def finish(self):
        """Mark trace as complete."""
        self.end_time = time.time()
        self.total_duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the trace."""
        return {
            "trace_id": self.trace_id,
            "total_duration_ms": self.total_duration_ms,
            "total_spans": len(self.spans),
            "success_spans": sum(1 for s in self.spans if s.status == "success"),
            "error_spans": sum(1 for s in self.spans if s.status == "error"),
            "spans_by_type": self._count_by_type(),
        }

    def _count_by_type(self) -> Dict[str, int]:
        """Count spans by their name/type."""
        counts = {}
        for span in self.spans:
            counts[span.name] = counts.get(span.name, 0) + 1
        return counts


class Tracer:
    """
    Simple tracer for monitoring agent execution.

    Provides:
    - Automatic span creation and lifecycle management
    - Nested span support (parent-child relationships)
    - Trace persistence to JSON files
    - Summary statistics

    Usage:
        tracer = Tracer()

        with tracer.start_trace("security_query") as trace:
            with tracer.start_span("tool_call", parent=trace):
                # Do work
                pass
    """

    def __init__(self, output_dir: str = "traces"):
        """
        Initialize tracer.

        Args:
            output_dir: Directory to save trace files
        """
        self.output_dir = output_dir
        self.current_trace: Optional[Trace] = None
        self.current_span: Optional[Span] = None
        self._span_counter = 0
        self._trace_counter = 0

        # Create output directory
        import os
        os.makedirs(output_dir, exist_ok=True)

    def _generate_trace_id(self) -> str:
        """Generate unique trace ID."""
        self._trace_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"trace_{timestamp}_{self._trace_counter}"

    def _generate_span_id(self) -> str:
        """Generate unique span ID."""
        self._span_counter += 1
        return f"span_{self._span_counter}"

    @contextmanager
    def start_trace(self, name: str):
        """
        Start a new trace (top-level operation).

        Args:
            name: Name for this trace

        Yields:
            Trace: The created trace
        """
        trace_id = self._generate_trace_id()
        trace = Trace(trace_id=trace_id)
        self.current_trace = trace

        # Create root span
        root_span = Span(
            span_id=self._generate_span_id(),
            name=name,
            start_time=time.time(),
            attributes={"trace_id": trace_id, "is_root": True}
        )
        trace.add_span(root_span)

        try:
            yield trace
            root_span.finish(status="success")
        except Exception as e:
            root_span.finish(status="error", error=str(e))
            raise
        finally:
            trace.finish()
            self._save_trace(trace)
            self.current_trace = None

    @contextmanager
    def start_span(self, name: str, parent: Optional[Trace] = None, **attributes):
        """
        Start a new span (individual operation within a trace).

        Args:
            name: Name for this span
            parent: Parent trace (uses current_trace if not provided)
            **attributes: Additional metadata to attach to span

        Yields:
            Span: The created span
        """
        trace = parent or self.current_trace
        if not trace:
            raise ValueError("No active trace. Use start_trace() first.")

        span = Span(
            span_id=self._generate_span_id(),
            name=name,
            start_time=time.time(),
            parent_id=self.current_span.span_id if self.current_span else None,
            attributes=attributes
        )
        trace.add_span(span)

        # Track parent-child relationship
        previous_span = self.current_span
        self.current_span = span

        try:
            yield span
            span.finish(status="success")
        except Exception as e:
            span.finish(status="error", error=str(e))
            raise
        finally:
            self.current_span = previous_span

    def _save_trace(self, trace: Trace):
        """Save trace to JSON file."""
        filename = f"{self.output_dir}/{trace.trace_id}.json"

        # Convert to dict for JSON serialization
        trace_dict = {
            "trace_id": trace.trace_id,
            "start_time": datetime.fromtimestamp(trace.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(trace.end_time).isoformat() if trace.end_time else None,
            "total_duration_ms": trace.total_duration_ms,
            "summary": trace.get_summary(),
            "spans": [
                {
                    **asdict(span),
                    "start_time": datetime.fromtimestamp(span.start_time).isoformat(),
                    "end_time": datetime.fromtimestamp(span.end_time).isoformat() if span.end_time else None,
                }
                for span in trace.spans
            ]
        }

        with open(filename, 'w') as f:
            json.dump(trace_dict, f, indent=2)

        print(f"\n✓ Trace saved: {filename}")
        print(f"  Duration: {trace.total_duration_ms}ms")
        print(f"  Spans: {len(trace.spans)}")
        print(f"  Status: {trace.spans[0].status if trace.spans else 'unknown'}")

    def print_trace_summary(self, trace: Trace):
        """Print a human-readable summary of the trace."""
        print("\n" + "=" * 70)
        print(f"TRACE SUMMARY: {trace.trace_id}")
        print("=" * 70)

        summary = trace.get_summary()
        print(f"\nOverall:")
        print(f"  Total Duration: {summary['total_duration_ms']}ms")
        print(f"  Total Spans: {summary['total_spans']}")
        print(f"  Success: {summary['success_spans']}, Errors: {summary['error_spans']}")

        print(f"\nSpan Breakdown:")
        for span_type, count in summary['spans_by_type'].items():
            print(f"  {span_type}: {count}")

        print(f"\nDetailed Timeline:")
        for i, span in enumerate(trace.spans, 1):
            indent = "  " if span.parent_id else ""
            status_icon = "✓" if span.status == "success" else "✗"
            print(f"{indent}[{i}] {status_icon} {span.name} ({span.duration_ms}ms)")
            if span.attributes:
                for key, value in span.attributes.items():
                    if key not in ['trace_id', 'is_root']:
                        print(f"{indent}    {key}: {value}")

        print("=" * 70 + "\n")


# Global tracer instance
_global_tracer: Optional[Tracer] = None


def get_tracer(output_dir: str = "traces") -> Tracer:
    """Get or create the global tracer instance."""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer(output_dir=output_dir)
    return _global_tracer
