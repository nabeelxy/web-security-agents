# Chapter 1: Introduction to LLM Agents for Security

## What You'll Learn

By the end of this chapter, you'll understand:
- What LLM agents are and how they differ from traditional automation
- Why security operations need intelligent agents
- The fundamental architecture of agent systems
- How Google ADK simplifies agent development
- How to set up your development environment
- How to build your first security agent in 10 lines of code

## Why Security Needs Intelligent Agents

### The Web Security Triage Problem

Imagine you're a web security analyst. Your morning inbox looks like this:

```
09:00 AM - 342 suspicious newly registered domains from NRD feeds (potential threats)
09:15 AM - 89 suspicious domains from Certificate Transparency logs
09:30 AM - 43 phishing emails reported by users
09:45 AM - 28 third-party blog posts flagging potential threats
10:00 AM - 5 customer complaints about false positives blocking legitimate sites
10:15 AM - 29 customer reports claiming false negatives (threats we missed)
```

You have 8 hours to investigate **536 web security items**. That's **less than 1 minute per item**.

**Traditional Approach:**
```
For each suspicious item:
  1. Check newly registered domain → analyze registration date, patterns
  2. Review Certificate Transparency logs → investigate SSL cert requests
  3. Copy domain to VirusTotal → wait for results (often no data yet)
  4. Check WHOIS → analyze registrar, privacy protection
  5. Visit URLScan.io → capture screenshot (if site is live)
  6. Search threat feeds → check known bad lists
  7. Verify reported phishing email → analyze headers, links
  8. Read third-party blog post → assess credibility, verify IOCs
  9. Investigate false positive → understand why it was blocked
  10. Research false negative → verify if threat was real
  11. Document findings → write assessment
  12. Make decision: block, allow, monitor, or update rules

Time per item: 15-20 minutes
Items handled per day: ~30 out of 536 (94% backlog!)
```

**With an Intelligent Agent:**
```
For each web security item:
  1. Send to agent: "Analyze new domain suspicious-site.com" or
     "Review CT log entry" or "Validate phishing report" or
     "Verify false positive claim"
  2. Agent automatically (in parallel):
     - Analyzes newly registered domain patterns (typosquatting, keywords)
     - Reviews Certificate Transparency log entries
     - Queries VirusTotal for domain reputation
     - Checks WHOIS for registration details, age, registrar
     - Scans with URLScan for screenshots (if site is live)
     - Searches threat intelligence feeds
     - Analyzes phishing email headers/links
     - Validates third-party blog claims and IOCs
     - Investigates false positive/negative reports
     - Correlates all findings with historical data
     - Generates comprehensive assessment with confidence score
  3. Review agent's verdict and evidence
  4. Make final decision with full context

Time per item: 1-2 minutes (agent works in parallel on batches)
Items handled per day: 400-480 out of 536 (10% backlog vs 94%)
```

**Impact:** 15-20x more items investigated, proactive threat detection from NRD/CT feeds, faster response to emerging threats, reduced analyst burnout, significantly better detection accuracy.

---

## What Are LLM Agents?

### Beyond Chatbots

You've probably used ChatGPT or similar LLM chatbots. They're impressive for conversations, but they have limitations:

| Capability | Chatbot | LLM Agent |
|-----------|---------|-----------|
| Answer questions | ✅ Yes | ✅ Yes |
| Access real-time data | ❌ No | ✅ Yes (via tools) |
| Take actions | ❌ No | ✅ Yes |
| Multi-step reasoning | ⚠️ Limited | ✅ Yes |
| Learn from tools | ❌ No | ✅ Yes |
| Specialized expertise | ⚠️ Generic | ✅ Domain-specific |

**Example - Chatbot:**
```
You: "Is malicious-domain.com safe?"
Chatbot: "I don't have real-time access to security databases.
          I recommend checking VirusTotal or similar services."
```

**Example - Agent:**
```
You: "Is malicious-domain.com safe?"
Agent:
  [Thinking] I need to check multiple threat intelligence sources
  [Action] Querying VirusTotal API...
  [Action] Checking WHOIS records...
  [Action] Scanning with URLScan.io...
  [Reasoning] 8/90 security vendors flag this as malicious,
              domain registered 3 days ago, typosquatting PayPal
  [Response] "MALICIOUS - High confidence phishing site"
```

### The Agent Architecture

Every LLM agent follows this fundamental architecture:

<img width="1454" height="550" alt="llm_agent" src="https://github.com/user-attachments/assets/de69b5d6-541a-4a8a-9309-2226cb695cf3" />

**1. Perception**
- Receives user queries
- Processes tool outputs
- Understands context and history - This could be from short or long term memory or RAG solutions

**2. Reasoning**
- Analyzes the situation
- Plans multi-step solutions
- Decides which tools to use
- Evaluates results

**3. Action**
- Executes tool calls
- Retrieves information
- Performs analysis
- Generates responses

### A Concrete Example: Domain Analysis

Let's trace how an agent analyzes a malicious domain:
<img width="1316" height="839" alt="agent_trace" src="https://github.com/user-attachments/assets/297a313a-a25f-4218-ab84-e85ee76c5bdc" />

This entire workflow happens automatically in seconds.

---

## Web Security Use Cases for LLM Agents

### 1. Newly Registered Domain (NRD) Analysis

**Traditional:** Manually review hundreds of new domains daily  
**With Agent:** Automated bulk analysis with pattern detection

```python
# Agent analyzes newly registered domains from NRD feeds
result = agent.analyze_new_domain("netlfix-mp.com")

# Output:
{
  "domain": "netlfix-mp.com",
  "verdict": "MALICIOUS",
  "confidence": 0.98,
  "threat_type": "Phishing - Brand Impersonation",
  "registration_details": {
    "registered": "2025-01-14 (4 days ago)",
    "registrar": "Tucows",
    "privacy_protected": true,
    "registrant_country": "Saint Kitts and Nevis"
  },
  "indicators": [
    "Combosquatting: mimics 'netflix.com' (combining -mp)",
    "High-value brand target: Netflix",
    "Privacy protection + recent registration = suspicious pattern",
    "VirusTotal: 3/97 vendors flag as phishing",
    "URLScan: Fake Netflix login page detected",
    "SSL cert issued same day as domain registration",
    "Threat Intel: Similar domains in active phishing campaign (PhishTank)"
  ],
  "recommendation": "Block immediately - active phishing campaign targeting Netflix users",
  "priority": "CRITICAL"
}
```

### 2. Phishing Email Analysis

**Traditional:** Manual examination of email headers, links, and content
**With Agent:** Comprehensive automated analysis

```python
# Agent analyzes reported phishing emails
verdict = agent.analyze_phishing_email(email_content)

# Output:
{
  "verdict": "PHISHING",
  "confidence": 0.96,
  "phishing_type": "Credential Harvesting",
  "indicators": [
    "Sender spoofing: Display 'PayPal' but from paypal-verify.com",
    "Urgency tactics: 'Verify account within 24h or suspension'",
    "Suspicious links: 3 links to paypal-verify.com/verify",
    "HTML mimics legitimate PayPal styling",
    "Embedded form requests username/password",
    "SSL cert mismatch on landing page"
  ],
  "affected_users": 43,
  "recommendation": "Quarantine all instances, notify affected users, block domain"
}
```

### 3. Third-Party Threat Report Validation

**Traditional:** Read blog posts and manually verify claims
**With Agent:** Automated validation with source correlation

```python
# Agent validates third-party reports (blogs, forums, social media)
validation = agent.validate_threat_report(
    source="security-blog.com/malicious-campaign-2025",
    claimed_iocs=["evil-domain.xyz", "185.220.101.47"]
)

# Output:
{
  "source_credibility": "HIGH",
  "validation_status": "CONFIRMED",
  "verified_iocs": [
    {
      "ioc": "evil-domain.xyz",
      "status": "MALICIOUS",
      "confirmed_by": ["VirusTotal: 45/90", "Threat Intel: Listed in 3 feeds"],
      "first_seen": "2025-01-10"
    },
    {
      "ioc": "185.220.101.47",
      "status": "MALICIOUS",
      "confirmed_by": ["AbuseIPDB: Confidence 98%", "Shodan: C2 server detected"],
      "associated_malware": "RedLine Stealer"
    }
  ],
  "recommendation": "Block all IOCs - active threat campaign confirmed",
  "priority": "HIGH"
}
```

### 4. False Positive Investigation

**Traditional:** Manual review of customer complaints about blocked sites
**With Agent:** Rapid investigation with evidence collection

```python
# Agent investigates customer-reported false positives
investigation = agent.investigate_false_positive(
    domain="legitimate-business.com",
    customer_complaint="Can't access our vendor's website - blocked by your filter",
    current_classification="SUSPICIOUS"
)

# Output:
{
  "verdict": "FALSE POSITIVE - SAFE",
  "confidence": 0.91,
  "original_block_reason": "New domain with privacy-protected WHOIS",
  "investigation_findings": [
    "Domain age: 45 days (just passed typical threshold)",
    "WHOIS: Privacy protected BUT valid business registration",
    "Company verification: legitimate-business.com matches registered LLC",
    "VirusTotal: 0/90 vendors flag issues",
    "URLScan: Professional business website, HTTPS valid",
    "No threat intel matches",
    "Customer provided business documentation"
  ],
  "recommendation": "Unblock and whitelist - legitimate business",
  "suggested_action": "Update detection rules to reduce similar false positives",
  "notify_customer": "Issue resolved, site now accessible"
}
```

### 5. False Negative Verification

**Traditional:** Manually investigate customer reports of missed threats
**With Agent:** Rapid threat validation and gap analysis

```python
# Agent verifies customer-reported false negatives
verification = agent.verify_false_negative(
    domain="bank-fake.net",
    customer_complaint="This phishing site wasn't blocked - I almost got scammed!",
    current_classification="SAFE"
)

# Output:
{
  "verdict": "FALSE NEGATIVE - MALICIOUS",
  "confidence": 0.89,
  "threat_confirmed": True,
  "investigation_findings": [
    "Domain age: 2 days (slipped through age-based rules)",
    "VirusTotal: 8/90 vendors NOW flag as phishing (wasn't detected during initial scan)",
    "URLScan: Screenshot reveals fake banking login page",
    "Threat Intel: Added to PhishTank 6 hours ago",
    "Similar to known campaign: typosquatting major bank"
  ],
  "detection_gap": "Time delay between domain creation and threat feed updates",
  "recommendation": "Block immediately, update rules to catch similar patterns",
  "suggested_improvements": [
    "Lower threshold for new domains with banking keywords",
    "Implement visual similarity detection for login pages",
    "Add real-time URLScan integration"
  ],
  "notify_customer": "Thank you for reporting - threat now blocked"
}
```

---

## The Google ADK Framework

### Why Google ADK?

Building agents from scratch is complex. You need:
- LLM integration
- Tool calling infrastructure
- Planning and reasoning logic
- Error handling
- State management
- Deployment infrastructure

**Google ADK (Agent Development Kit)** provides all of this out of the box.

### ADK vs Other Frameworks

| Feature | Google ADK | LangChain | AutoGPT |
|---------|-----------|-----------|---------|
| Built-in planner | ✅ ReAct | ⚠️ Manual | ✅ Auto |
| Tool integration | ✅ Simple | ✅ Extensive | ⚠️ Limited |
| Production-ready | ✅ Yes | ⚠️ Needs work | ❌ Experimental |
| Google AI native | ✅ Yes | ⚠️ Adapter | ❌ No |
| Learning curve | ✅ Easy | ⚠️ Moderate | ⚠️ Steep |
| Documentation | ✅ Excellent | ✅ Good | ⚠️ Limited |

**Why we chose ADK for this book:**
1. **Simplicity** - Build agents in minutes, not hours
2. **Production-ready** - Battle-tested at Google scale
3. **Native Gemini** - Direct access to latest Google AI models
4. **Built-in planning** - ReAct pattern out of the box
5. **MCP support** - Standard tool protocol

### ADK Architecture

<img width="1086" height="584" alt="adk_architecture" src="https://github.com/user-attachments/assets/a08eea25-0590-4a3b-8186-2351ed809eb7" />


---

## Setting Up Your Development Environment

### Prerequisites

Before we begin, ensure you have:

1. **Python 3.10 or higher**
   ```bash
   python --version
   # Should show: Python 3.10.x or higher
   ```

2. **pip (Python package manager)**
   ```bash
   pip --version
   ```

3. **Google Cloud Account** (free tier works fine with the $300 credit provided by GCP at the time of writing)
   - Sign up at: https://cloud.google.com

4. **Google AI API Key**
   - Get it from: https://aistudio.google.com/apikey
   - Click "Create API Key"
   - Copy and save it securely

### Installation Steps

**Step 1: Install Google ADK**

Recommened to create a virtual environment first:
```bash
python -m venv venv
source venv/bin/activate
```
Then install the necessary libraries in the virtual environment:
```bash
pip install google-adk google-genai
```

This installs:
- `google-adk` - Agent Development Kit
- `google-genai` - Gemini API client

**Step 2: Configure API Key**

Create a `.env` file in your project directory:

```bash
# .env file
GOOGLE_API_KEY=your_api_key_here
```

**Important:** Never commit API keys to version control!

Add to `.gitignore`:
```
.env
```

**Step 3: Verify Installation**

Create a test file `test_setup.py`:

```python
from google import genai
import os

# Test API connection
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Say hello!'
)
print(response.text)
```

Run it:
```bash
python test_setup.py
```

Expected output:
```
Hello!
```

If you see this, you're ready to build agents! 

### Development Tools (Optional but Recommended)

**VS Code Extensions:**
- Python (Microsoft)
- Pylance (Microsoft)
- Python Indent (Kevin Rose)

**Useful Python Packages:**
```bash
pip install python-dotenv  # Load .env files
pip install black          # Code formatting
pip install pylint         # Code linting
```

---

## Your First Security Agent in less than 10 Lines

Let's build a simple security Q&A agent to understand the basics.

### The Code
Create a folder first_agent  
cd first_agent. 
Create .env with the following env variables:  
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<your_api_key_here>
```
Create `agent.py`:

```python
from google.adk.agents import LlmAgent

# Create agent with security expertise
root_agent = LlmAgent(
    name="security_advisor",
    model="gemini-2.5-flash",
    instruction="""You are an expert cybersecurity advisor.
    Provide clear, accurate security guidance."""
)
```

### Running Your First Agent

```bash
cd .. # Go to the parent folder
adk web
```

This should start the adk web server and you should see something similar to the following:

```
+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://127.0.0.1:8000.                         |
+-----------------------------------------------------------------------------+
```

Go to your favovrite browser and access the above URL. Let's ask what prompt
injection is. 

You should see a reply similar to the following:  
<img width="1359" height="636" alt="adk_web_example1" src="https://github.com/user-attachments/assets/8f6e63a1-79ff-49e0-a19f-4aedbfdfa89a" />


### Understanding the Code

Let's break down what's happening:

```python
from google.adk.agents import LlmAgent
```
- Imports the agent class from Google ADK

```python
root_agent = LlmAgent(
    name="security_advisor",
    model="gemini-2.5-flashp",
    instruction="You are an expert cybersecurity advisor..."
)
```
- **name**: Identifier for your agent (we use the name root_agent to comply with adk web discovery logic. You may also create root_agent.yaml file instead if you want to use a different name and specify in this yaml file.
- **model**: Which Gemini model to use
  - `gemini-2.5-flash` - Fast, cost-effective (recommended if you are on a tight budget)
  - `gemini-3.0-pro-preview` - Most capable at the time of writing, but more expensive. Check out [Google's model page](https://ai.google.dev/gemini-api/docs/models) for more information and latest updates.
- **instruction**: System prompt defining agent behavior and expertise

---

## Understanding Agent Behavior Through Instructions

The `instruction` parameter is crucial - it defines your agent's personality, expertise, and behavior.

### Example 1: Generic Assistant (Vague)

```python
agent = LlmAgent(
    name="assistant",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful assistant."
)

result = agent.run("Is paypa1.com safe?")
print(result.get("result"))
```

**Output:**
```
I don't have access to real-time security databases. I recommend
checking the domain through VirusTotal or similar services.
```

**Problem:** Too generic, not actionable.

### Example 2: Security Expert (Better)

```python
agent = LlmAgent(
    name="security_analyst",
    model="gemini-2.0-flash-exp",
    instruction="""You are an expert security analyst specializing
    in threat detection and domain analysis.

    When analyzing domains:
    1. Check for typosquatting patterns
    2. Consider domain age and registration details
    3. Look for suspicious patterns
    4. Provide clear verdicts: SAFE, SUSPICIOUS, or MALICIOUS
    5. Explain your reasoning
    """
)

result = agent.run("Is paypa1.com safe?")
print(result.get("result"))
```

**Output:**
```
VERDICT: SUSPICIOUS - Likely Malicious

REASONING:
1. Typosquatting: paypa1.com mimics paypal.com (1 vs l)
2. This is a common phishing technique
3. Legitimate PayPal uses paypal.com, not variations

RECOMMENDATION: Do not visit this site. It's likely a phishing
page designed to steal PayPal credentials.

To verify:
- Check WHOIS registration date (likely very recent)
- Scan with VirusTotal
- Report to anti-phishing organizations
```

**Much better!** Specific, actionable, expert-level analysis.

### Example 3: Structured Output

```python
agent = LlmAgent(
    name="domain_analyzer",
    model="gemini-2.0-flash-exp",
    instruction="""You are a domain security analyzer.

    Analyze domains and respond in this JSON format:
    {
      "domain": "...",
      "verdict": "SAFE|SUSPICIOUS|MALICIOUS",
      "confidence": 0.0-1.0,
      "indicators": ["list", "of", "findings"],
      "recommendation": "..."
    }
    """
)

result = agent.run("Analyze: paypa1.com")
print(result.get("result"))
```

**Output:**
```json
{
  "domain": "paypa1.com",
  "verdict": "MALICIOUS",
  "confidence": 0.92,
  "indicators": [
    "Typosquatting: resembles paypal.com",
    "Substitution attack: '1' replacing 'l'",
    "Known phishing technique"
  ],
  "recommendation": "Block immediately and report to users"
}
```

**Key Lesson:** Good instructions = good results. We'll master this in Chapter 2.

---

## Beyond Simple Q&A: The Power of Tools

Our current agent can only reason based on its training. It can't:
- ❌ Check VirusTotal in real-time
- ❌ Perform WHOIS lookups
- ❌ Access current threat intelligence
- ❌ Scan websites

In Chapter 3, we'll add tools to give our agent superpowers:

```python
# Preview of what's coming
agent = LlmAgent(
    name="web_security_agent",
    model="gemini-2.0-flash-exp",
    instruction="...",
    tools=[
        whois_lookup_tool,
        virustotal_scan_tool,
        urlscan_tool,
        threat_intel_tool
    ]
)

# Now the agent can take real actions!
result = agent.run("Analyze paypa1.com")

# Agent automatically:
# 1. Runs WHOIS lookup
# 2. Scans with VirusTotal
# 3. Captures screenshot via URLScan
# 4. Checks threat intelligence databases
# 5. Correlates all findings
# 6. Generates comprehensive report
```

But first, we need to master prompt engineering in Chapter 2.

---

## Key Takeaways

**✅ What We Learned:**

1. **LLM Agents vs Chatbots**
   - Agents can use tools to access real-time data
   - Agents can take actions, not just answer questions
   - Agents follow multi-step reasoning patterns

2. **Agent Architecture**
   - Perception: Understanding inputs and context
   - Reasoning: Planning and decision-making
   - Action: Tool execution and response generation

3. **Security Use Cases**
   - Alert triage (5-7x faster)
   - Phishing analysis
   - Threat intelligence enrichment
   - Incident response automation
   - Vulnerability assessment

4. **Google ADK Framework**
   - Simplifies agent development
   - Production-ready out of the box
   - Native Gemini integration
   - Built-in ReAct planner

5. **Instructions Matter**
   - Good instructions = expert-level results
   - Specificity and structure improve output
   - We'll master this in Chapter 2

**✅ What You Can Do Now:**

- Set up a development environment
- Create basic security advisory agents
- Understand agent architecture
- Recognize when agents add value

**✅ What's Next:**

Chapter 2: **Prompt Engineering for Security Agents**
- Transform vague agents into precise security analysts
- Master few-shot learning and chain-of-thought
- Structure outputs for automation
- Debug and improve agent responses

---

## Hands-On Exercises

### Exercise 1: Build Your Own Security Advisor

Create an agent that specializes in a specific security domain:

```python
from google.adk.agents import LlmAgent

# Choose a specialty:
# - Malware analysis
# - Network security
# - Cloud security
# - Application security

agent = LlmAgent(
    name="YOUR_SPECIALTY_advisor",
    model="gemini-2.0-flash-exp",
    instruction="""
    # Define your agent's expertise here
    """
)

# Test with 5 questions in your domain
questions = [
    "Question 1...",
    # Add 4 more
]

for q in questions:
    result = agent.run(q)
    print(f"Q: {q}")
    print(f"A: {result.get('result')}\n")
```

**Success Criteria:**
- Agent provides accurate, expert-level responses
- Answers are specific to your security domain
- Output is actionable and clear

### Exercise 2: Improve Agent Instructions

Start with this vague agent:

```python
agent = LlmAgent(
    name="analyzer",
    model="gemini-2.0-flash-exp",
    instruction="Analyze security things."
)
```

**Your task:** Rewrite the instruction to make the agent:
1. Specialize in incident analysis
2. Provide structured outputs (severity, impact, recommendations)
3. Ask clarifying questions when needed
4. Explain reasoning clearly

**Test query:** "We detected unusual outbound traffic from server-42"

**Compare:**
- Before (vague instruction): Generic response
- After (specific instruction): Structured, actionable analysis

### Exercise 3: Agent Comparison

Create three agents with different models and compare:

```python
agent_flash = LlmAgent(
    name="flash_agent",
    model="gemini-2.0-flash-exp",
    instruction="Expert security analyst"
)

agent_pro = LlmAgent(
    name="pro_agent",
    model="gemini-2.0-pro-exp",
    instruction="Expert security analyst"
)

# Same instruction, different models
test_query = "Explain how ransomware encrypts files"

flash_result = agent_flash.run(test_query)
pro_result = agent_pro.run(test_query)

# Compare:
# - Response quality
# - Level of detail
# - Speed
# - Which is better for your use case?
```

---

## Discussion Questions

1. **When NOT to use agents?**
   - What security tasks are better suited for traditional automation?
   - When is deterministic behavior more important than intelligence?

2. **Ethics and responsibility:**
   - Should agents make autonomous security decisions?
   - Where should humans stay in the loop?
   - How do we audit agent decisions?

3. **Cost vs value:**
   - If an agent costs $0.001 per query, but saves 15 minutes of analyst time, what's the ROI?
   - How many alerts justify investing in agent automation?

4. **Security of agents:**
   - What happens if an attacker can manipulate your agent's instructions?
   - How do you prevent agents from leaking sensitive information?
   - (We'll address this in Chapter 10: Safety and Security)

---

## Additional Resources

**Official Documentation:**
- Google ADK: https://google.github.io/adk/
- Gemini API: https://ai.google.dev/docs
- Google AI Studio: https://aistudio.google.com

**Security Agent Use Cases:**
- MITRE ATT&CK Framework: https://attack.mitre.org/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- OWASP Top 10: https://owasp.org/www-project-top-ten/

**Community:**
- Google ADK GitHub: https://github.com/google/adk
- Security Automation Community: https://www.reddit.com/r/netsecstudents/

---

## What's Next?

In **Chapter 2: Prompt Engineering for Security Agents**, you'll learn:

- How to write system prompts that create expert-level security analysts
- Few-shot learning: Teaching agents through examples
- Chain-of-thought: Making agents show their reasoning
- Structured outputs: JSON, tables, and custom formats
- Debugging: Fixing vague or incorrect agent responses

The difference between a basic agent and an expert analyst is 90% prompt engineering. Let's master it.

**See you in Chapter 2!** 🚀
