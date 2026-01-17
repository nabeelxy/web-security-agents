# Lesson 9: Prompt Engineering

This lesson teaches the fundamentals of prompt engineering for AI agents. Learn how to craft effective prompts that produce consistent, high-quality outputs.

## What You'll Learn

- System vs user prompts and when to use each
- Few-shot learning with examples
- Chain-of-thought reasoning for complex tasks
- Prompt templates with variables
- Debugging poor outputs through iteration
- Production-ready prompt patterns

## Why Prompt Engineering Matters

**The Reality:**
- 80% of agent quality comes from prompt engineering
- Poor prompts → inconsistent, unreliable outputs
- Good prompts → predictable, production-ready behavior
- Time spent on prompts saves debugging time later

**Impact:**
- Better prompts improve accuracy more than better models
- Proper prompting reduces hallucinations
- Clear structure enables automated parsing
- Examples teach patterns faster than instructions

## Key Concepts

### 1. System vs User Prompts

**System Prompt:**
- Defines agent's role, behavior, constraints
- Sets global context for all interactions
- Like "permanent instructions"
- Example: "You are a security expert specializing in..."

**User Prompt:**
- Specific task or question
- Changes with each interaction
- Like "current request"
- Example: "Analyze this domain: example.com"

### 2. Few-Shot Learning

Teaching by example:
```
Example 1: google.com → SAFE (official domain)
Example 2: g00gle.com → SAFE (defensive registration)
Example 3: goowle.com → DANGEROUS (typosquatting)
Example 4: google-deals.com → SUSPICIOUS (unclear legitimacy)

Now analyze: [new domain]
```

Few-shot learning:
- Shows desired output format
- Teaches reasoning patterns
- Improves consistency
- Reduces need for explicit instructions

### 3. Chain-of-Thought (CoT)

Guide step-by-step reasoning:
```
Step 1: Check domain structure
Step 2: Analyze brand impersonation
Step 3: Review technical indicators
Step 4: Synthesize verdict

Now analyze: [domain]
```

Benefits:
- Breaks complex tasks into steps
- Makes reasoning transparent
- Reduces logical errors
- Easier to debug failures

### 4. Prompt Templates

Reusable prompts with variables:
```python
def create_prompt(domain, context, user_level):
    return f"""
    Analyze {domain}
    Context: {context}
    Expertise: {user_level}
    ...
    """
```

Advantages:
- Consistency across queries
- Easy A/B testing
- Centralized improvements
- Parameterized complexity

### 5. Structured Output

Enforce format for parsing:
```
VERDICT: [SAFE|SUSPICIOUS|DANGEROUS]
CONFIDENCE: [Low|Medium|High]
REASONING: [explanation]
RECOMMENDATION: [action]
```

Why structure matters:
- Programmatically parseable
- Consistent field presence
- Easier validation
- Better for automation

## Files Overview

| File | Purpose |
|------|---------|
| [prompts.py](prompts.py) | Comprehensive prompt library with examples |
| [compare_prompts.py](compare_prompts.py) | Side-by-side comparison of techniques |
| [iterate_prompts.py](iterate_prompts.py) | Debugging workflow through iterations |

## Quick Start

### 1. Explore the Prompt Library

```bash
python prompts.py
```

**Output:**
- Examples of different prompting techniques
- Before/after comparisons
- Template usage examples

### 2. Compare Prompting Strategies

```bash
python compare_prompts.py --run
```

**What it does:**
- Runs same domain through different prompts
- Shows output differences
- Analyzes quality improvements

**Sample output:**
```
======================================================================
COMPARISON 1: BASIC vs OPTIMIZED SYSTEM PROMPT
======================================================================

Test Domain: paypa1-verify.com

BASIC SYSTEM PROMPT: "You are a security expert."
Response:
This domain looks suspicious. The number 1 is replacing the letter 'l'.

─────────────────────────────────────────────────────────────────────

OPTIMIZED SYSTEM PROMPT:
"You are a web security expert specializing in domain reputation analysis..."

Response:
Risk Level: DANGEROUS

Key Indicators:
- Character substitution (1 for l) - typosquatting PayPal
- "verify" keyword - credential harvesting attempt
- Domain mimics paypal.com structure

Recommendation: DO NOT VISIT. This is a phishing site. Report to PayPal.
```

### 3. See Prompt Iteration in Action

```bash
python iterate_prompts.py --run
```

**What it shows:**
- Starting with minimal prompt (fails)
- Adding structure (better but incomplete)
- Adding methodology (getting there)
- Adding examples (production-ready!)

## Prompt Engineering Patterns

### Pattern 1: Basic → Optimized

**❌ Basic (Poor):**
```python
instruction = "You are a security expert."
```

Problems:
- No clear task definition
- No output format specified
- No quality criteria
- Inconsistent responses

**✅ Optimized (Good):**
```python
instruction = """You are a web security expert specializing in domain reputation.

Your role:
- Analyze domains for threats (phishing, malware, typosquatting)
- Provide clear risk assessments (SAFE, SUSPICIOUS, DANGEROUS)
- Explain reasoning with specific indicators
- Give actionable recommendations

Always structure your response as:
1. Risk Level: [SAFE/SUSPICIOUS/DANGEROUS]
2. Key Indicators: [Specific red flags or trust signals]
3. Recommendation: [What the user should do]"""
```

Benefits:
- Clear role definition
- Explicit task breakdown
- Structured output format
- Actionable guidance

### Pattern 2: Add Few-Shot Examples

**❌ Without Examples:**
```python
query = "Analyze this domain for security threats."
```

**✅ With Examples:**
```python
query = """Analyze domains for security threats. Examples:

Domain: google.com
Risk: SAFE
Indicators: Official Google domain, .com TLD, established brand
Action: This is legitimate

Domain: g00gle.com
Risk: DANGEROUS
Indicators: Character substitution (0→o), typosquatting
Action: Phishing attempt, do not visit

Now analyze: {domain}"""
```

### Pattern 3: Chain-of-Thought for Complex Analysis

**❌ Direct Question:**
```python
query = "Is this domain safe?"
```

**✅ With CoT:**
```python
query = """Analyze step-by-step:

Step 1: Domain Structure
- Check for character substitutions
- Look for suspicious keywords
- Examine TLD

Step 2: Brand Analysis
- Does it mimic a known brand?
- Spelling variations?

Step 3: Technical Indicators
- Domain age
- SSL certificate
- Threat feeds

Step 4: Verdict
- Weigh all indicators
- Determine risk level

Domain: {domain}"""
```

### Pattern 4: Structured Output Enforcement

**❌ Free-form:**
```python
instruction = "Analyze domain security and tell me what you think."
```

**✅ Structured:**
```python
instruction = """Analyze domain and respond in this EXACT format:

VERDICT: [Must be SAFE, SUSPICIOUS, or DANGEROUS]
CONFIDENCE: [Low, Medium, or High]
INDICATORS:
- [Specific finding 1]
- [Specific finding 2]
RECOMMENDATION: [Clear action]

Do not deviate from this format."""
```

### Pattern 5: Prevent Hallucinations

**❌ Hallucination-Prone:**
```python
query = "What's the security reputation of {domain}?"
```
→ Agent may invent WHOIS data, threat scores, etc.

**✅ Grounded:**
```python
query = """Analyze {domain} based ONLY on observable patterns:
1. Domain name structure
2. Visual similarity to known brands
3. Keyword presence

DO NOT make claims about:
- Domain age (unless provided)
- WHOIS data (unless provided)
- Threat scores (unless provided)

If you don't have data, say "Unable to determine without additional data"

Domain: {domain}"""
```

## Real-World Examples

### Example 1: Typosquatting Detection

**Poor Prompt:**
```
"Is paypa1.com safe?"
```

**Optimized Prompt:**
```python
"""Analyze this domain for typosquatting:

TYPOSQUATTING INDICATORS:
- Character substitution (0/o, 1/l, rn/m)
- Missing characters (micros0ft)
- Extra characters (gooogle)
- Wrong TLD (google.co instead of google.com)
- Homoglyphs (аpple.com with Cyrillic 'а')

EXAMPLES:
paypal.com → SAFE (original)
paypa1.com → DANGEROUS (1 substitutes l)
paypai.com → SUSPICIOUS (missing l)

Domain to analyze: paypa1.com

Format:
VERDICT: [SAFE|SUSPICIOUS|DANGEROUS]
TECHNIQUE: [Which typosquatting method, if any]
ORIGINAL: [What domain is being mimicked]
ACTION: [What user should do]
```

### Example 2: Context-Aware Analysis

**Poor Prompt:**
```
"Check amazon-support.com"
```

**Optimized Prompt:**
```python
"""Analyze this domain received in a suspicious email:

CONTEXT: User received email claiming Amazon account locked,
asking them to click link to "amazon-support.com" to verify

PHISHING INDICATORS FOR THIS CONTEXT:
- Urgency tactics (account locked, verify now)
- Non-official domain mimicking brand
- Requesting sensitive info
- Came via unsolicited email

OFFICIAL AMAZON DOMAINS:
- amazon.com, amazon.co.uk, amazon.de, etc.
- NOT: amazon-support, amazon-verify, amazonpay-secure

Domain: amazon-support.com
Context: Email claims account locked

Assess if this is phishing and explain why.
```

### Example 3: Technical vs Non-Technical Users

**For Technical Users:**
```python
"""Analyze {domain}

Provide technical details:
- WHOIS registration data interpretation
- DNS record analysis (A, MX, TXT records)
- SSL certificate chain validation
- Threat intelligence correlation
- Historical domain reputation

Include technical evidence for your verdict.
"""
```

**For General Users:**
```python
"""Analyze {domain}

Explain in simple terms:
- Is it safe? (Yes/No)
- Why? (1-2 sentences in plain English)
- What should I do? (Clear action)

Avoid technical jargon.
"""
```

## Prompt Debugging Workflow

When agent outputs are poor, follow this workflow:

### Step 1: Identify the Problem

Common issues:
- **Inconsistent format** → Add structure enforcement
- **Wrong verdicts** → Add few-shot examples
- **Vague reasoning** → Add chain-of-thought
- **Hallucinations** → Add explicit constraints
- **Too verbose** → Add length limits
- **Missing fields** → Enforce structured output

### Step 2: Isolate the Cause

Test with simpler prompts:
```python
# Remove complexity to find the issue
# If it works with simple prompt, gradually add back pieces
```

### Step 3: Iterate

```
Version 1: Minimal → Identify failures
Version 2: + Structure → Better but incomplete
Version 3: + Examples → Consistent format
Version 4: + Constraints → Production-ready
```

### Step 4: A/B Test

```python
# Compare old vs new prompt
for domain in test_cases:
    old_result = run_with_old_prompt(domain)
    new_result = run_with_new_prompt(domain)
    compare(old_result, new_result)
```

### Step 5: Validate at Scale

```bash
# Run evaluation suite (from L07)
python run_eval.py
```

## Best Practices

### DO:

✅ **Start with examples** - Show, don't just tell
✅ **Be specific** - "Analyze for phishing" > "Check security"
✅ **Enforce format** - Define exact output structure
✅ **Add constraints** - "Based only on X" prevents hallucinations
✅ **Test edge cases** - Tricky domains reveal prompt weaknesses
✅ **Version prompts** - Track changes like code
✅ **A/B test** - Compare before making changes permanent

### DON'T:

❌ **Don't be vague** - "Security expert" is too general
❌ **Don't assume** - Agent won't infer desired format
❌ **Don't skip examples** - Instructions alone aren't enough
❌ **Don't ignore failures** - Each failure reveals prompt gaps
❌ **Don't over-complicate** - Start simple, add complexity as needed
❌ **Don't forget context** - Domain analysis needs domain knowledge

## Production Prompts

For production systems, combine all techniques:

```python
PRODUCTION_PROMPT = """
[SYSTEM ROLE]
You are a web security analyst specialized in domain reputation.

[METHODOLOGY]
Follow this analysis framework:
1. Structural analysis (typos, keywords, TLD)
2. Brand analysis (impersonation patterns)
3. Technical indicators (when available)
4. Risk synthesis

[CONSTRAINTS]
- Base analysis ONLY on observable patterns
- Don't claim facts without evidence
- Distinguish between "likely" and "proven"

[OUTPUT FORMAT]
RISK_LEVEL: [SAFE|SUSPICIOUS|DANGEROUS]
KEY_INDICATORS:
- [Finding 1]
- [Finding 2]
CONFIDENCE: [Low|Medium|High]
RECOMMENDATION: [Clear action]
REASONING: [1-2 sentences]

[EXAMPLES]
[Include 3-5 diverse examples showing edge cases]

Now analyze:
"""
```

## Integration with Other Lessons

### L01: Basic Agents
→ Start here after L01 to build solid foundations

### L02: Tool Calling
→ Prompts guide when/how to use tools

### L06: ReAct Agent
→ Prompts structure the reasoning loop

### L07: Evaluations
→ Test prompt improvements systematically

### L08: Observability
→ Track prompt performance in production

## Advanced Topics

### Prompt Chains

For complex tasks, chain prompts:
```python
# Prompt 1: Extract key info
extract = "List all suspicious indicators in {domain}"

# Prompt 2: Analyze findings
analyze = "Based on {indicators}, assess risk"

# Prompt 3: Generate recommendation
recommend = "Given {risk}, what should user do?"
```

### Dynamic Prompts

Adapt prompts based on context:
```python
def get_prompt(domain, user_expertise, has_whois_data):
    base = get_base_prompt()

    if user_expertise == "beginner":
        base += "\nExplain in simple terms."

    if has_whois_data:
        base += "\nInclude WHOIS analysis."

    return base
```

### Prompt Versioning

Track prompt evolution:
```python
PROMPT_V1 = "Basic instructions"  # 60% accuracy
PROMPT_V2 = "+ Structure"         # 75% accuracy
PROMPT_V3 = "+ Examples"          # 85% accuracy
PROMPT_V4 = "+ Constraints"       # 92% accuracy

# Use in production with version tracking
current_prompt = PROMPT_V4
```

## Summary

You've learned:
- ✅ System vs user prompts
- ✅ Few-shot learning with examples
- ✅ Chain-of-thought reasoning
- ✅ Prompt templates and variables
- ✅ Debugging through iteration
- ✅ Production-ready patterns

**Key Insight:** Prompt engineering is not an afterthought—it's the foundation of reliable AI agents. Invest time here to save debugging time later.

## Further Reading

- **OpenAI Prompt Engineering Guide**: https://platform.openai.com/docs/guides/prompt-engineering
- **Anthropic Prompt Library**: https://docs.anthropic.com/en/prompt-library
- **Google Gemini Prompting Guide**: https://ai.google.dev/gemini-api/docs/prompting-strategies
- **Chain-of-Thought Paper**: https://arxiv.org/abs/2201.11903
- **Few-Shot Learning**: https://arxiv.org/abs/2005.14165
