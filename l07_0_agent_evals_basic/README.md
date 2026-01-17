# Lesson 7.0 - Agent Evaluations (Basic)

This lesson demonstrates how to build evaluation datasets and run systematic evaluations to measure agent quality. Evaluation (evals) is critical for ensuring agent reliability, catching regressions, and measuring improvements over time.

## What You'll Learn

- How to design comprehensive evaluation datasets
- Writing test cases with expected outcomes
- Running automated evaluations against agents
- Interpreting evaluation results and metrics
- Identifying failure patterns and areas for improvement
- Comparing evaluation runs to track progress

## Why Evaluations Matter

**Without evals:**
- No objective measure of agent quality
- Regressions go unnoticed
- Improvements are hard to quantify
- Production issues discovered by users

**With evals:**
- Quantifiable metrics (accuracy, latency)
- Catch bugs before deployment
- Track improvements over time
- Build confidence in agent behavior

## Key Concepts

### Evaluation Dataset

A structured collection of test cases, each with:
- **Input**: Query or task for the agent
- **Expected output**: What the agent should produce
- **Category**: Type of test (legitimate, phishing, edge case)
- **Metadata**: Additional context for analysis

### Evaluation Metrics

- **Accuracy**: Percentage of correct responses
- **Category breakdown**: Performance by test type
- **Latency**: Average response time
- **Error rate**: Failed executions

### Continuous Evaluation

- Run evals before every deployment
- Track metrics over time
- Compare runs to measure improvements
- Build regression test suites

## Prerequisites

```bash
pip install google-adk google-genai
```

## Environment Setup

Ensure your `.env` file includes:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

## Files Overview

| File | Purpose | Run When |
|------|---------|----------|
| [security_agent.py](security_agent.py) | Agent being evaluated | - |
| [create_eval_dataset.py](create_eval_dataset.py) | Creates test cases | Once, or when adding tests |
| [run_eval.py](run_eval.py) | Runs evaluations | After agent changes |
| [analyze_results.py](analyze_results.py) | Analyzes failures | After eval runs |

## Workflow

### Step 1: Create Evaluation Dataset

```bash
python create_eval_dataset.py
```

This creates `eval_dataset.json` with ~20 test cases covering:
- **Legitimate domains** (google.com, microsoft.com)
- **Typosquatting** (g00gle.com, paypal-login.com)
- **Phishing** (paypal-secure-login.xyz)
- **Edge cases** (gooogle.com, apple.co)

**Example test case:**
```json
{
  "id": "safe_001",
  "category": "legitimate",
  "input": "Is google.com safe?",
  "expected_verdict": "SAFE",
  "expected_reasoning": "google.com is a well-known legitimate domain",
  "notes": "Top brand, should be immediately recognized"
}
```

### Step 2: Run Evaluations

```bash
python run_eval.py
```

**What happens:**
1. Loads the evaluation dataset
2. Creates the security agent
3. Runs each test case
4. Extracts verdicts from responses
5. Compares actual vs expected
6. Calculates metrics
7. Saves results to `eval_results.json`

**Sample output:**
```
==================================================================
SECURITY AGENT EVALUATION
==================================================================

Loading dataset from: eval_dataset.json
✓ Loaded 20 test cases

Initializing security agent...
✓ Agent ready

Running evaluations...
------------------------------------------------------------------
[1/20] safe_001: ✓ PASS (SAFE) - 1.23s
[2/20] safe_002: ✓ PASS (SAFE) - 0.87s
[3/20] typo_001: ✓ PASS (SUSPICIOUS) - 1.45s
[4/20] typo_002: ✗ FAIL (expected SUSPICIOUS, got SAFE) - 1.12s
...
------------------------------------------------------------------

EVALUATION SUMMARY
==================================================================
Total Tests:      20
Passed:           17
Failed:           3
Accuracy:         85.00%
Avg Latency:      1.15s

CATEGORY BREAKDOWN
------------------------------------------------------------------
legitimate            5/ 5 (100.0%)
typosquatting         3/ 4 ( 75.0%)
phishing              4/ 4 (100.0%)
edge_case             3/ 4 ( 75.0%)
phrasing_variation    2/ 2 (100.0%)

✓ Results saved to: eval_results.json
```

### Step 3: Analyze Results

```bash
python analyze_results.py
```

**What it does:**
- Identifies failure patterns
- Groups errors by type
- Shows category-specific issues
- Generates recommendations
- Saves detailed report to `eval_report.txt`

**Sample analysis:**
```
FAILURE ANALYSIS
==================================================================
Total Failures: 3

ERROR PATTERNS
------------------------------------------------------------------

SUSPICIOUS → SAFE (2 cases):
  • typo_002: Should I trust paypal-login.com?
    Response: PayPal-login.com appears to be related to PayPal...
  • edge_003: Should I visit apple.co?
    Response: Apple.co is likely safe, as .co domains are common...

SUSPICIOUS → UNKNOWN (1 case):
  • edge_001: Is gooogle.com safe?
    Response: I cannot determine if gooogle.com is safe...

CATEGORY-SPECIFIC FAILURES
------------------------------------------------------------------

typosquatting (1 failure):
  • typo_002: Expected SUSPICIOUS, got SAFE

edge_case (2 failures):
  • edge_001: Expected SUSPICIOUS, got UNKNOWN
  • edge_003: Expected SUSPICIOUS, got SAFE
```

## Understanding the Agent

The security agent ([security_agent.py:1-56](security_agent.py#L1-L56)) is intentionally simple:

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="security_assessor",
    model="gemini-2.0-flash",
    description="Web security expert for domain safety assessment.",
    instruction="""You are a web security expert assistant...

Categorize domains as:
- SAFE: Well-known legitimate domains
- SUSPICIOUS: Potential typosquatting or unclear legitimacy
- DANGEROUS: Clear phishing or malicious attempts"""
)
```

**No external tools** - purely in-context learning
**Why?** - Focuses eval on agent reasoning, not tool availability

## Evaluation Dataset Design

A good eval dataset should:

### 1. Cover Core Scenarios

- **Happy path**: Expected inputs with clear answers
- **Edge cases**: Unusual but valid inputs
- **Error cases**: Invalid or problematic inputs

### 2. Test Boundaries

- Exact matches (google.com)
- Near misses (g00gle.com)
- Extreme cases (very long domains, unusual TLDs)

### 3. Include Variations

- Different phrasings ("Is X safe?" vs "Should I trust X?")
- Different domains in same category
- Same domain with different contexts

### 4. Be Representative

- Reflect real-world distribution
- Include common failure modes
- Test critical security scenarios

## Interpreting Results

### Accuracy Thresholds

| Accuracy | Assessment | Action |
|----------|------------|--------|
| 95%+ | Excellent | Production-ready |
| 85-94% | Good | Review failures, consider deployment |
| 70-84% | Moderate | Significant improvements needed |
| <70% | Poor | Major redesign required |

### Category Performance

If a category has <80% accuracy:
- Review test case quality (are they clear?)
- Check agent instructions (does it know how to handle this?)
- Add examples to instructions
- Consider adding tools/knowledge base

### Latency Considerations

- **<1s**: Excellent responsiveness
- **1-3s**: Acceptable for most use cases
- **3-5s**: May need optimization
- **>5s**: User experience issue

## Common Failure Patterns

### 1. Overly Conservative

**Pattern:** Marks legitimate domains as SUSPICIOUS
**Fix:** Add positive examples to instructions
**Example:** "microsoft.com is safe, even if unfamiliar to some users"

### 2. Overly Permissive

**Pattern:** Marks phishing as SAFE
**Fix:** Strengthen threat detection instructions
**Example:** "Domains like paypal-login.com are NEVER legitimate PayPal"

### 3. Inconsistent Verdicts

**Pattern:** Same category gets different verdicts
**Fix:** Make instructions more explicit
**Example:** "ALL typosquatting attempts are at least SUSPICIOUS"

### 4. Missing Keywords

**Pattern:** Verdict is correct but keyword not in response
**Fix:** Explicitly request keyword in instructions
**Example:** "Always include your verdict: SAFE, SUSPICIOUS, or DANGEROUS"

## Improving Agent Performance

### Iteration Cycle

1. **Run eval** → Identify failures
2. **Analyze patterns** → Understand root causes
3. **Update agent** → Fix instructions or add tools
4. **Re-run eval** → Measure improvement
5. **Compare results** → Ensure no regressions

### Agent Improvement Strategies

**Add Examples:**
```python
instruction="""
Examples:
- google.com → SAFE (well-known brand)
- g00gle.com → SUSPICIOUS (typosquatting)
- google-login.xyz → DANGEROUS (phishing)
"""
```

**Make Criteria Explicit:**
```python
instruction="""
Mark as DANGEROUS if:
- Uses unusual TLD with brand name (.xyz, .tk)
- Includes fake security terms (secure-, verify-)
- Combines brand names (amazonpaypal.com)
"""
```

**Add Reasoning Requirements:**
```python
instruction="""
Always explain:
1. What made you suspicious
2. What indicators you found
3. Your final verdict
"""
```

## Advanced Evaluation Techniques

### A/B Testing

Compare two agent versions:

```bash
# Run baseline
python run_eval.py  # Creates eval_results.json

# Make changes to agent

# Run improved version
python run_eval.py  # Creates new eval_results.json (rename old first)

# Compare
python analyze_results.py --compare eval_results_v1.json eval_results_v2.json
```

### Expanding the Dataset

Add new test cases to `create_eval_dataset.py`:

```python
{
    "id": "custom_001",
    "category": "custom_category",
    "input": "Your test input",
    "expected_verdict": "SAFE|SUSPICIOUS|DANGEROUS",
    "expected_reasoning": "Why this verdict",
    "notes": "Context for this test"
}
```

### Automated Regression Testing

Run evals in CI/CD:

```bash
# In your CI pipeline
python create_eval_dataset.py
python run_eval.py
python analyze_results.py

# Fail build if accuracy < threshold
if [ $(jq '.summary.accuracy_percent' eval_results.json) -lt 85 ]; then
    echo "Accuracy below threshold!"
    exit 1
fi
```

## Production Evaluation Workflow

### 1. Development

- Run evals locally during development
- Quick iteration on failing tests
- Achieve target accuracy before PR

### 2. Testing

- Automated eval run in CI
- Block merge if accuracy drops
- Compare with baseline metrics

### 3. Staging

- Run evals against staging environment
- Include production-like data
- Validate performance metrics

### 4. Production

- Continuous evaluation with sample traffic
- Monitor accuracy over time
- Alert on metric degradation

## Evaluation Best Practices

### DO:

✅ **Start small** - Begin with 10-20 high-quality test cases
✅ **Test boundaries** - Focus on edge cases and common failures
✅ **Version datasets** - Track changes to eval sets over time
✅ **Automate** - Run evals automatically before deployments
✅ **Track metrics** - Monitor accuracy, latency, error rates
✅ **Iterate** - Continuously improve agent based on failures

### DON'T:

❌ **Over-fit** - Don't tune agent just to pass specific tests
❌ **Ignore context** - Consider real-world usage patterns
❌ **Stop at one run** - Single runs can be misleading
❌ **Forget latency** - Accuracy without speed is insufficient
❌ **Skip documentation** - Document why tests exist

## Common Issues

**"Agent passes locally but fails in eval"**
- Check for randomness (temperature settings)
- Ensure consistent environment (API keys, model version)
- Review test case clarity

**"Accuracy varies between runs"**
- LLMs have inherent randomness
- Set temperature=0 for deterministic results
- Run multiple times and average

**"Test cases are too easy"**
- Good! Start easy and add harder cases
- Focus on failure modes from production
- Test boundaries, not just happy paths

**"Don't know what verdict to expect"**
- Ask: "What would a security expert say?"
- Consult security guidelines
- When unsure, test both options

## Real-World Application

This basic eval framework extends to:

### Security Agent with Tools (L06)

- Test tool selection (does it call WHOIS for domain age?)
- Test tool output usage (does it correctly interpret VT scores?)
- Test multi-tool orchestration (does it combine evidence properly?)

### Multi-Agent Systems (L05)

- Test agent coordination
- Test output passing between agents
- Test error handling in pipelines

### RAG Systems (L04)

- Test retrieval quality (does it find relevant docs?)
- Test answer grounding (does it cite sources correctly?)
- Test hallucination prevention

## Next Steps

After mastering basic evals:

1. **Add more test cases** - Expand to 50-100 cases
2. **Test with tools** - Evaluate L06 capstone agent
3. **Build golden dataset** - Curate high-quality reference set
4. **Automate in CI** - Run on every commit
5. **Track over time** - Build performance dashboards

## Additional Resources

- [Google ADK Testing Guide](https://google.github.io/adk/testing/)
- [Anthropic Evals Guide](https://docs.anthropic.com/en/docs/test-and-evaluate)
- [OpenAI Evals Framework](https://github.com/openai/evals)

## Summary

You've learned how to:
- ✅ Create structured evaluation datasets
- ✅ Run automated agent evaluations
- ✅ Calculate accuracy and latency metrics
- ✅ Analyze failures and identify patterns
- ✅ Iterate on agent improvements
- ✅ Build confidence in agent quality

Evaluations are the foundation of reliable AI systems. Use this framework to ensure your agents work correctly before deploying to production.
