# Lesson 8.0 - Agent Observability and Tracing

This lesson demonstrates how to add observability to AI agents through distributed tracing. Learn to monitor agent behavior, track performance, and debug issues in production systems.

## What You'll Learn

- Core observability concepts: traces, spans, and attributes
- How to instrument agents with tracing
- Capturing tool calls and execution flow
- Analyzing performance bottlenecks
- Building simple observability without external dependencies

## Why Observability Matters

**Without observability:**
- No visibility into agent behavior
- Can't identify performance issues
- Difficult to debug failures
- No data for optimization

**With observability:**
- Understand what agents are doing
- Identify slow operations
- Debug failures with context
- Optimize based on data
- Build confidence for production

## Key Concepts

### Distributed Tracing

Tracing follows a request through a distributed system:

- **Trace**: Complete execution of one agent invocation
- **Span**: Individual operation within a trace (tool call, LLM request, etc.)
- **Attributes**: Metadata attached to spans (tool name, duration, status, etc.)

### Why Tracing for Agents?

Agents are complex systems:
- Multiple LLM calls (planning, tool use, refinement)
- Tool invocations (APIs, databases, searches)
- Async operations
- Non-deterministic behavior

Tracing helps you understand:
- Which tools are called and when
- How long each operation takes
- Where failures occur
- Patterns in agent behavior

## Files Overview

| File | Purpose |
|------|---------|
| [tracer.py](tracer.py) | Simple tracing implementation |
| [security_agent.py](security_agent.py) | Agent with Google Search tool |
| [run_agent.py](run_agent.py) | Instrumented agent runner |
| [analyze_traces.py](analyze_traces.py) | Trace analysis tool |

## Quick Start

### 1. Run Agent with Tracing

```bash
# Run with default demo queries
python run_agent.py

# Or run with custom query
python run_agent.py "What is XSS and how to prevent it?"
```

**Output:**
- Agent responses to your queries
- Real-time trace summaries
- Trace files saved to `traces/` directory

### 2. Analyze Traces

```bash
# Analyze all traces
python analyze_traces.py
```

**Sample output:**
```
======================================================================
TRACE ANALYSIS
======================================================================

📊 Overall Statistics:
  Total traces: 2
  Total execution time: 8543.21ms
  Average execution time: 4271.61ms
  Successful: 2/2 (100.0%)

🔍 Span Analysis:
  Span Type Breakdown:
    agent_execution:
      Count: 2
      Avg Duration: 3847.32ms
      Total Duration: 7694.64ms
    tool_call:
      Count: 3
      Avg Duration: 245.18ms
      Total Duration: 735.54ms
    agent_setup:
      Count: 2
      Avg Duration: 52.11ms
      Total Duration: 104.22ms

🔧 Tool Usage:
  google_search:
    Invocations: 3
    Avg Duration: 245.18ms

⚡ Performance Insights:
  Slowest Traces:
    1. trace_20250117_142530_1: 4821.45ms
       Bottleneck: agent_execution (4125.32ms)
```

### 3. Examine Individual Traces

Trace files are saved as JSON in `traces/`:

```bash
cat traces/trace_20250117_142530_1.json
```

**Example trace structure:**
```json
{
  "trace_id": "trace_20250117_142530_1",
  "start_time": "2025-01-17T14:25:30.123456",
  "total_duration_ms": 4821.45,
  "summary": {
    "total_spans": 5,
    "success_spans": 5,
    "error_spans": 0
  },
  "spans": [
    {
      "span_id": "span_1",
      "name": "agent_invocation",
      "duration_ms": 4821.45,
      "status": "success",
      "attributes": {
        "trace_id": "trace_20250117_142530_1",
        "is_root": true
      }
    },
    {
      "span_id": "span_2",
      "parent_id": "span_1",
      "name": "agent_setup",
      "duration_ms": 54.32,
      "status": "success"
    },
    {
      "span_id": "span_3",
      "parent_id": "span_1",
      "name": "format_query",
      "duration_ms": 0.21,
      "status": "success",
      "attributes": {
        "query": "What are the top 3 web security vulnerabilities?"
      }
    },
    {
      "span_id": "span_4",
      "parent_id": "span_1",
      "name": "agent_execution",
      "duration_ms": 4125.32,
      "status": "success",
      "attributes": {
        "response_length": 1243,
        "tool_calls": 1
      }
    },
    {
      "span_id": "span_5",
      "parent_id": "span_1",
      "name": "tool_call",
      "duration_ms": 312.45,
      "status": "success",
      "attributes": {
        "tool_name": "google_search",
        "tool_call_number": 1
      }
    }
  ]
}
```

## Understanding the Tracer

### Basic Usage

```python
from tracer import get_tracer

# Get global tracer instance
tracer = get_tracer(output_dir="traces")

# Start a trace
with tracer.start_trace("agent_invocation") as trace:

    # Add spans for individual operations
    with tracer.start_span("tool_call", parent=trace, tool_name="search"):
        # Do work
        result = search_api.call()

    with tracer.start_span("llm_call", parent=trace, tokens=150):
        # Call LLM
        response = llm.generate()

# Trace automatically saved when context exits
```

### Span Hierarchy

Spans can be nested to represent parent-child relationships:

```
Trace: agent_invocation (4821ms)
  ├─ Span: agent_setup (54ms)
  ├─ Span: format_query (0.2ms)
  ├─ Span: agent_execution (4125ms)
  │   └─ Span: tool_call (312ms)
  └─ Span: response_formatting (12ms)
```

This hierarchy shows:
- Overall agent took 4821ms
- Most time spent in agent_execution (4125ms)
- Tool call within execution took 312ms
- Setup and formatting were fast

### Attributes

Attach metadata to spans for debugging:

```python
with tracer.start_span("tool_call",
                       tool_name="whois_lookup",
                       domain="example.com",
                       cache_hit=False) as span:
    result = whois_lookup("example.com")
    span.attributes["result_size"] = len(result)
```

Attributes help answer questions:
- Which tool was called?
- What were the inputs?
- Was cache used?
- How much data returned?

## Production Observability

This lesson demonstrates core concepts with a simple file-based tracer. For production:

### Use Production Tracing Systems

**Popular Options:**
- **OpenTelemetry** - Industry standard, vendor-agnostic
- **LangSmith** - Built for LLM applications
- **Weights & Biases** - Great for ML/AI tracking
- **DataDog APM** - Full-featured commercial solution
- **Jaeger** - Open-source distributed tracing

### OpenTelemetry Example

OpenTelemetry is the industry standard:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter

# Setup OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to Jaeger
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Use in code
with tracer.start_as_current_span("agent_call") as span:
    span.set_attribute("query", query)
    result = agent.run(query)
    span.set_attribute("response_length", len(result))
```

### LangSmith Example

LangSmith is purpose-built for LLM applications:

```python
from langsmith import Client
from langchain.callbacks.tracers import LangChainTracer

# Initialize LangSmith
client = Client()
tracer = LangChainTracer(project_name="security-agent")

# LangChain automatically instruments with callback
agent.run(
    query,
    callbacks=[tracer]
)
# Traces appear in LangSmith UI automatically
```

## What to Trace

### Essential Metrics

1. **Agent Invocations**
   - Total duration
   - Success/failure rate
   - Query type/category

2. **Tool Calls**
   - Which tools used
   - Tool latency
   - Tool success rate
   - Input/output sizes

3. **LLM Calls**
   - Number of calls per invocation
   - Token usage
   - Model used
   - Latency

4. **Errors**
   - Error type
   - Error location (which span)
   - Error context
   - Stack traces

### Example Instrumentation

```python
async def run_traced_agent(query: str):
    with tracer.start_trace("agent_invocation") as trace:

        # Track setup
        with tracer.start_span("setup", parent=trace):
            agent = create_agent()

        # Track planning
        with tracer.start_span("planning", parent=trace) as span:
            plan = agent.plan(query)
            span.attributes["steps"] = len(plan)

        # Track execution
        with tracer.start_span("execution", parent=trace) as span:
            for step in plan:
                with tracer.start_span("step", parent=trace,
                                     step_type=step.type):
                    if step.type == "tool":
                        with tracer.start_span("tool_call", parent=trace,
                                             tool=step.tool_name):
                            result = await step.execute()
                    elif step.type == "llm":
                        with tracer.start_span("llm_call", parent=trace) as llm_span:
                            response = await llm.generate()
                            llm_span.attributes["tokens"] = response.tokens

        # Track response formatting
        with tracer.start_span("formatting", parent=trace):
            final_response = format_response(result)

        return final_response
```

## Analysis and Optimization

### Identify Bottlenecks

Run analysis to find slow operations:

```bash
python analyze_traces.py
```

Look for:
- **High average duration** - Consistently slow operations
- **High total duration** - Operations called frequently
- **Outliers** - Occasional very slow calls

### Common Optimizations

**If tool calls are slow:**
- Add caching
- Parallelize independent calls
- Use faster alternatives
- Pre-fetch common data

**If LLM calls are slow:**
- Reduce prompt size
- Use faster models for simple tasks
- Add streaming for better UX
- Cache common responses

**If agent setup is slow:**
- Lazy load tools
- Reuse agent instances
- Pre-initialize expensive resources

### A/B Testing

Compare different implementations:

```bash
# Run version A
python run_agent.py "test query"
# Note trace_id from output

# Run version B (with changes)
python run_agent.py "test query"
# Note trace_id from output

# Compare traces
python analyze_traces.py trace_A_id trace_B_id
```

## Real-World Example

Let's trace a security analysis workflow:

```python
async def analyze_domain_with_tracing(domain: str):
    tracer = get_tracer()

    with tracer.start_trace("domain_analysis") as trace:

        # WHOIS lookup
        with tracer.start_span("whois", parent=trace, domain=domain) as span:
            whois_data = await whois_lookup(domain)
            span.attributes["registrar"] = whois_data.get("registrar")
            span.attributes["age_days"] = whois_data.get("age_days")

        # VirusTotal check
        with tracer.start_span("virustotal", parent=trace, domain=domain) as span:
            vt_score = await virustotal_check(domain)
            span.attributes["score"] = vt_score
            span.attributes["malicious"] = vt_score > 5

        # Screenshot analysis
        with tracer.start_span("screenshot", parent=trace, domain=domain) as span:
            screenshot = await capture_screenshot(domain)
            span.attributes["size_bytes"] = len(screenshot)

            with tracer.start_span("vision_analysis", parent=trace) as vision_span:
                analysis = await vision_model.analyze(screenshot)
                vision_span.attributes["tokens"] = analysis.tokens

        # LLM synthesis
        with tracer.start_span("llm_synthesis", parent=trace) as span:
            report = await llm.synthesize(whois_data, vt_score, analysis)
            span.attributes["report_length"] = len(report)
            span.attributes["verdict"] = report.verdict

        tracer.print_trace_summary(trace)
        return report
```

This gives visibility into:
- Which operations are slowest
- If any tools are failing
- Token usage patterns
- End-to-end latency

## Best Practices

### DO:

✅ **Trace at operation boundaries** - Major steps like tool calls, LLM requests
✅ **Add relevant attributes** - Enough context to debug issues
✅ **Track both success and failure** - Errors are just as important
✅ **Use consistent naming** - Makes analysis easier
✅ **Include timing information** - Essential for performance optimization
✅ **Sample in production** - Don't trace 100% in high-volume systems

### DON'T:

❌ **Don't trace too granularly** - Every function call is excessive
❌ **Don't log sensitive data** - PII, secrets, credentials
❌ **Don't ignore errors** - Failed spans are valuable
❌ **Don't forget to close spans** - Use context managers
❌ **Don't block on tracing** - Async/background export

## Extending This Example

To build production-ready observability:

1. **Add Metrics**
   - Counter: Total requests, tool calls, errors
   - Histogram: Latency distribution
   - Gauge: Active requests, queue depth

2. **Add Logging**
   - Structured logs with trace IDs
   - Correlation between logs and traces
   - Different log levels (debug, info, error)

3. **Add Alerting**
   - High error rates
   - Slow operations
   - Unusual patterns

4. **Build Dashboards**
   - Real-time metrics
   - Trace visualization
   - Performance trends

5. **Integrate with Production Tools**
   - OpenTelemetry for vendor neutrality
   - Export to Jaeger/Zipkin for visualization
   - Send to DataDog/NewRelic for alerting

## Further Reading

- **OpenTelemetry Documentation**: https://opentelemetry.io/docs/
- **LangSmith Guide**: https://docs.smith.langchain.com/
- **Distributed Tracing Concepts**: https://opentelemetry.io/docs/concepts/observability-primer/
- **Google Cloud Trace**: https://cloud.google.com/trace/docs
- **Production LLM Observability**: https://www.wandb.ai/site/solutions/llmops

## Summary

You've learned:
- ✅ Core observability concepts (traces, spans, attributes)
- ✅ How to instrument agents with tracing
- ✅ Capturing and analyzing execution flow
- ✅ Identifying performance bottlenecks
- ✅ Building towards production observability

Observability is essential for reliable AI systems. Start simple with file-based tracing, then migrate to production tools as you scale.
