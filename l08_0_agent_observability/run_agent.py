"""
Run Security Agent with Tracing

This script demonstrates how to instrument an agent with observability.
It captures:
- Overall agent execution time
- Individual tool calls
- Token usage (when available)
- Execution flow
"""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from security_agent import create_instrumented_agent
from tracer import get_tracer


async def run_agent_with_tracing(query: str):
    """
    Run the agent with full tracing enabled.

    Args:
        query: Security question to ask the agent
    """
    tracer = get_tracer(output_dir="traces")

    # Start a trace for this agent invocation
    with tracer.start_trace("agent_invocation") as trace:

        # Track agent setup
        with tracer.start_span("agent_setup", parent=trace):
            agent = create_instrumented_agent()
            session_service = InMemorySessionService()

            await session_service.create_session(
                app_name="security_agent_traced",
                user_id="trace_user",
                session_id="trace_session"
            )

            runner = Runner(
                app_name="security_agent_traced",
                agent=agent,
                session_service=session_service
            )

        # Track query formatting
        with tracer.start_span("format_query", parent=trace, query=query):
            content = types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )

        # Track agent execution
        with tracer.start_span("agent_execution", parent=trace) as exec_span:
            events = runner.run_async(
                new_message=content,
                user_id="trace_user",
                session_id="trace_session"
            )

            response_text = None
            tool_calls = 0

            async for event in events:
                # Track tool calls
                if hasattr(event, 'tool_calls') and event.tool_calls:
                    for tool_call in event.tool_calls:
                        tool_calls += 1
                        with tracer.start_span(
                            "tool_call",
                            parent=trace,
                            tool_name=getattr(tool_call, 'name', 'unknown'),
                            tool_call_number=tool_calls
                        ):
                            # Tool execution happens inside the runner
                            pass

                # Capture final response
                if event.is_final_response():
                    response_text = event.content.parts[0].text
                    exec_span.attributes["response_length"] = len(response_text)
                    exec_span.attributes["tool_calls"] = tool_calls
                    break

        # Allow cleanup
        await asyncio.sleep(0.1)

        # Print results
        print("\n" + "=" * 70)
        print("AGENT RESPONSE")
        print("=" * 70)
        print(f"\nQuery: {query}")
        print(f"\nResponse:\n{response_text}")
        print("\n" + "=" * 70)

        # Print trace summary
        tracer.print_trace_summary(trace)

        return response_text


async def run_multiple_queries():
    """Run multiple queries to demonstrate tracing across invocations."""
    queries = [
        "What are the top 3 web security vulnerabilities in 2025?",
        "How does SQL injection work?",
    ]

    print("=" * 70)
    print("RUNNING MULTIPLE QUERIES WITH TRACING")
    print("=" * 70)
    print(f"\nWill execute {len(queries)} queries")
    print("Each query will generate a separate trace file\n")

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"QUERY {i}/{len(queries)}")
        print(f"{'='*70}\n")

        await run_agent_with_tracing(query)

        # Brief pause between queries
        if i < len(queries):
            print("\nWaiting before next query...\n")
            await asyncio.sleep(1)

    print("\n" + "=" * 70)
    print("ALL QUERIES COMPLETED")
    print("=" * 70)
    print("\nCheck the 'traces/' directory for detailed trace files")
    print("Each file contains:")
    print("  - Complete execution timeline")
    print("  - Tool call details")
    print("  - Duration metrics")
    print("  - Nested span relationships")


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        # Run with custom query from command line
        query = " ".join(sys.argv[1:])
        print(f"\nRunning with query: {query}\n")
        asyncio.run(run_agent_with_tracing(query))
    else:
        # Run demo with multiple queries
        asyncio.run(run_multiple_queries())


if __name__ == "__main__":
    main()
