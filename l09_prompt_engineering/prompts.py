"""
Prompt Engineering Examples

This module demonstrates different prompting techniques for security agents:
- Basic vs optimized system prompts
- Few-shot learning
- Chain-of-thought reasoning
- Prompt templates with variables
"""

# ==============================================================================
# 1. SYSTEM vs USER PROMPTS
# ==============================================================================

# BAD: Vague system prompt
BASIC_SYSTEM_PROMPT = """You are a security expert."""

# GOOD: Detailed system prompt with clear instructions
OPTIMIZED_SYSTEM_PROMPT = """You are a web security expert specializing in domain reputation analysis.

Your role:
- Analyze domains for security threats (phishing, malware, typosquatting)
- Provide clear risk assessments (SAFE, SUSPICIOUS, DANGEROUS)
- Explain your reasoning with specific indicators
- Give actionable recommendations

Always structure your response as:
1. Risk Level: [SAFE/SUSPICIOUS/DANGEROUS]
2. Key Indicators: [List specific red flags or trust signals]
3. Recommendation: [What the user should do]"""


# ==============================================================================
# 2. FEW-SHOT LEARNING
# ==============================================================================

# BAD: No examples, agent must figure out format
NO_EXAMPLES_PROMPT = """Analyze this domain for security threats."""

# GOOD: Few-shot examples teach the agent desired behavior
FEW_SHOT_PROMPT = """Analyze domains for security threats. Follow these examples:

Example 1:
Domain: google.com
Analysis:
- Risk Level: SAFE
- Key Indicators:
  • Established brand (founded 1998)
  • Valid SSL certificate
  • Tranco top 10 domain
  • No typosquatting patterns
- Recommendation: This is the legitimate Google domain. Safe to visit.

Example 2:
Domain: g00gle-login.xyz
Analysis:
- Risk Level: DANGEROUS
- Key Indicators:
  • Character substitution (0 for o) - classic typosquatting
  • Suspicious TLD (.xyz commonly used for phishing)
  • Contains "login" - credential harvesting attempt
  • Domain age: 3 days old
- Recommendation: DO NOT VISIT. This is a phishing site impersonating Google.

Example 3:
Domain: amaz0n-support.com
Analysis:
- Risk Level: SUSPICIOUS
- Key Indicators:
  • Typosquatting attempt (0 instead of o)
  • Uses "support" keyword - social engineering tactic
  • Recently registered domain
  • Not listed in Amazon's official domains
- Recommendation: Avoid. Contact Amazon through official website (amazon.com).

Now analyze the following domain:"""


# ==============================================================================
# 3. CHAIN-OF-THOUGHT (CoT) PROMPTING
# ==============================================================================

# BAD: Direct question, no reasoning process
DIRECT_PROMPT = """Is this domain safe?"""

# GOOD: Chain-of-thought prompting guides reasoning
CHAIN_OF_THOUGHT_PROMPT = """Analyze this domain step-by-step:

Step 1: Domain Structure Analysis
- Check for character substitutions (0 for o, 1 for l, etc.)
- Look for unusual TLDs (.xyz, .tk, .ml)
- Identify suspicious keywords (login, verify, secure, account)

Step 2: Brand Impersonation Check
- Does it mimic a known brand?
- Are there spelling variations?
- Does it combine brand names unusually?

Step 3: Technical Indicators
- Domain age (newer = more suspicious)
- SSL certificate validity
- WHOIS information
- Known threat feeds

Step 4: Synthesis
- Weigh all indicators
- Determine risk level
- Provide clear recommendation

Now analyze this domain:"""


# ==============================================================================
# 4. PROMPT TEMPLATES WITH VARIABLES
# ==============================================================================

def create_domain_analysis_prompt(
    domain: str,
    context: str = None,
    user_technical_level: str = "general"
) -> str:
    """
    Create a customized domain analysis prompt.

    Args:
        domain: Domain to analyze
        context: Optional context (e.g., "received in email", "clicked from ad")
        user_technical_level: "general" or "technical"

    Returns:
        Formatted prompt string
    """

    # Adjust explanation depth based on user
    if user_technical_level == "technical":
        depth_instruction = """Provide technical details including:
- WHOIS data interpretation
- DNS record analysis
- SSL certificate chain validation
- Threat intelligence source citations"""
    else:
        depth_instruction = """Explain in clear, non-technical language.
Focus on actionable advice for non-experts."""

    # Add context if provided
    context_section = ""
    if context:
        context_section = f"""
Context: {context}
Consider this context when assessing risk level."""

    prompt = f"""Analyze the security of this domain: {domain}
{context_section}

{depth_instruction}

Provide:
1. Risk Level (SAFE/SUSPICIOUS/DANGEROUS)
2. Clear explanation of why
3. Specific recommendation

Be concise but complete."""

    return prompt


def create_comparison_prompt(domain1: str, domain2: str) -> str:
    """Create prompt for comparing two domains."""
    return f"""Compare these two domains for security:

Domain A: {domain1}
Domain B: {domain2}

For each domain:
1. Identify security indicators
2. Assign risk level
3. Explain key differences

Then provide a comparative summary showing which is safer and why."""


def create_threat_hunting_prompt(domain: str, threat_type: str) -> str:
    """Create focused prompt for specific threat type."""

    threat_indicators = {
        "phishing": [
            "Credential harvesting keywords (login, verify, account)",
            "Brand impersonation patterns",
            "Urgent language in landing page",
            "Form fields requesting sensitive data"
        ],
        "malware": [
            "Known malware distribution domains",
            "Suspicious file download prompts",
            "Drive-by download techniques",
            "Exploit kit signatures"
        ],
        "typosquatting": [
            "Character substitutions (0/o, 1/l, rn/m)",
            "Missing or extra characters",
            "Different TLDs of popular domains",
            "Homograph attacks (unicode lookalikes)"
        ]
    }

    indicators = threat_indicators.get(threat_type, [])
    indicators_text = "\n".join(f"- {ind}" for ind in indicators)

    return f"""Analyze this domain specifically for {threat_type} threats: {domain}

Focus on these {threat_type} indicators:
{indicators_text}

Assessment:
1. Does this domain exhibit {threat_type} characteristics?
2. What specific indicators did you find?
3. Confidence level (Low/Medium/High)
4. Recommended action"""


# ==============================================================================
# 5. DEBUGGING POOR OUTPUTS
# ==============================================================================

# PROBLEM: Agent gives inconsistent verdicts
INCONSISTENT_PROMPT = """Is this domain safe? Answer yes or no."""

# SOLUTION: Structured output format
STRUCTURED_OUTPUT_PROMPT = """Analyze this domain and respond in this exact format:

VERDICT: [Must be exactly one of: SAFE | SUSPICIOUS | DANGEROUS]
CONFIDENCE: [Low | Medium | High]
REASONING: [2-3 sentence explanation]
RECOMMENDATION: [Specific action for user]

Domain to analyze:"""


# PROBLEM: Agent is too verbose
VERBOSE_PROMPT = """Tell me everything you can about this domain's security."""

# SOLUTION: Explicit constraints
CONCISE_PROMPT = """Analyze this domain's security in exactly 3 bullet points:
• Risk level and why (1 sentence)
• Most important indicator (1 sentence)
• What to do (1 sentence)

Domain:"""


# PROBLEM: Agent hallucinates facts
HALLUCINATION_PRONE_PROMPT = """What's the security reputation of this domain?"""

# SOLUTION: Explicit limitations and knowledge grounding
GROUNDED_PROMPT = """Analyze this domain based ONLY on these observable characteristics:
1. Domain name structure (typos, keywords, TLD)
2. Visual patterns (character substitution, brand similarity)

DO NOT make claims about:
- Domain age (unless explicitly provided)
- WHOIS data (unless explicitly provided)
- Threat feed listings (unless explicitly provided)

If you don't have information, say "Unable to determine without additional data"

Domain to analyze:"""


# ==============================================================================
# 6. ADVANCED: SYSTEM + EXAMPLES + CoT COMBINED
# ==============================================================================

PRODUCTION_PROMPT = """You are a web security analyst specialized in domain reputation assessment.

METHODOLOGY:
Follow this analysis framework for every domain:

1. STRUCTURAL ANALYSIS
   - Character patterns (substitutions, extra chars, missing chars)
   - TLD assessment (.com/.org = common, .xyz/.tk = risky)
   - Keyword detection (login, secure, verify, account)

2. BRAND ANALYSIS
   - Does it resemble a known brand?
   - What are the visual/textual similarities?
   - Is this likely intentional impersonation?

3. CONTEXTUAL INDICATORS
   - Domain composition (hyphens, numbers, length)
   - Suspicious keyword combinations
   - Common phishing patterns

4. RISK SYNTHESIS
   - Aggregate all indicators
   - Weigh severity of each indicator
   - Determine overall risk level

OUTPUT FORMAT:
RISK_LEVEL: [SAFE | SUSPICIOUS | DANGEROUS]
KEY_INDICATORS:
- [List 2-4 most important findings]
CONFIDENCE: [Low | Medium | High]
RECOMMENDATION: [Clear action for user]
REASONING: [1-2 sentences explaining the verdict]

EXAMPLES:

Input: paypal.com
RISK_LEVEL: SAFE
KEY_INDICATORS:
- Official PayPal domain
- Standard .com TLD
- No typosquatting patterns
CONFIDENCE: High
RECOMMENDATION: This is the legitimate PayPal website. Safe to use.
REASONING: This is the verified official domain for PayPal services.

Input: paypa1-secure.xyz
RISK_LEVEL: DANGEROUS
KEY_INDICATORS:
- Character substitution (1 for l) - typosquatting
- Suspicious keyword "secure" - social engineering
- High-risk TLD (.xyz)
- Brand impersonation (PayPal)
CONFIDENCE: High
RECOMMENDATION: DO NOT VISIT. Report as phishing.
REASONING: Multiple strong phishing indicators including typosquatting and suspicious TLD.

Now analyze the following domain:"""


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

if __name__ == "__main__":
    # Example 1: Basic vs optimized
    print("=" * 70)
    print("EXAMPLE 1: SYSTEM PROMPT COMPARISON")
    print("=" * 70)
    print("\nBASIC PROMPT:")
    print(BASIC_SYSTEM_PROMPT)
    print("\nOPTIMIZED PROMPT:")
    print(OPTIMIZED_SYSTEM_PROMPT)

    # Example 2: Few-shot learning
    print("\n" + "=" * 70)
    print("EXAMPLE 2: FEW-SHOT LEARNING")
    print("=" * 70)
    print(FEW_SHOT_PROMPT)

    # Example 3: Prompt templates
    print("\n" + "=" * 70)
    print("EXAMPLE 3: PROMPT TEMPLATES WITH VARIABLES")
    print("=" * 70)

    # Technical user
    tech_prompt = create_domain_analysis_prompt(
        domain="amaz0n-verify.com",
        context="Received in suspicious email",
        user_technical_level="technical"
    )
    print("\nFor Technical User:")
    print(tech_prompt)

    # General user
    general_prompt = create_domain_analysis_prompt(
        domain="amaz0n-verify.com",
        context="Received in suspicious email",
        user_technical_level="general"
    )
    print("\nFor General User:")
    print(general_prompt)

    # Example 4: Threat-specific prompt
    print("\n" + "=" * 70)
    print("EXAMPLE 4: THREAT-SPECIFIC PROMPTS")
    print("=" * 70)
    phishing_prompt = create_threat_hunting_prompt(
        "paypal-login.secure-verify.com",
        "phishing"
    )
    print(phishing_prompt)
