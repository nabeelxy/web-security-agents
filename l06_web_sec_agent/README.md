# Lesson 6 - Web Security Agent (Capstone)

This is the capstone project where all workshop learnings come together. You'll build a comprehensive, production-ready web security agent that combines multiple intelligence sources to provide thorough domain assessments using the ReAct planning pattern.

## What You'll Build

A security agent that can:
- **Analyze domain reputation** using Tranco rankings, Crunchbase, and malicious IP databases
- **Conduct WHOIS investigations** to identify registrar, age, and ownership
- **Leverage threat intelligence** from VirusTotal and URLScan.io
- **Perform visual analysis** of websites using screenshot analysis
- **Query historical context** from threat intelligence reports via RAG
- **Reason through complex assessments** using ReAct planning
- **Provide comprehensive verdicts** with supporting evidence

## What You'll Learn

- How to orchestrate multiple MCP tools in a single agent
- Implementing the ReAct (Reasoning + Acting) planning pattern
- Using Google ADK's BuiltInPlanner for autonomous tool selection
- Combining structured data (WHOIS, VT) with unstructured data (RAG, screenshots)
- Designing agent instructions that guide tool usage
- Managing thinking budgets for cost control
- Building production-ready security agents

## Architecture Overview

```
User Query: "Is paypal-login.com safe?"
    ↓
ReAct Agent (gemini-2.5-pro)
    ↓
┌─────────────── BuiltInPlanner ────────────────┐
│ Thinks: "I need reputation, WHOIS, VT, scan" │
│ Plans: Call tools in logical order           │
│ Acts: Executes tool calls                    │
│ Reflects: Synthesizes results                │
└───────────────────────────────────────────────┘
    ↓
┌─────── MCP Tools (from Lessons 3-5) ──────┐
│ • domain_reputation  (L06 custom tool)    │
│ • whois_lookup       (L03.0)              │
│ • virustotal_lookup  (L03.1)              │
│ • urlscan_scan       (L03.2)              │
│ • threat_intel_rag   (L04)                │
└───────────────────────────────────────────┘
    ↓
Final Assessment: "HIGH RISK - Phishing site..."
```

## Tools Used

This agent integrates tools from all previous lessons:

### 1. Domain Reputation Tool (NEW in L06)
**Source:** [tools/dominfo_server.py:1-56](tools/dominfo_server.py#L1-L56)
**Knowledge base:** [../../kb/](../../kb/) (~96MB of reputation data)

Checks:
- **Tranco ranking** - Is the domain in top 1M popular sites?
- **Crunchbase presence** - Is it a registered business?
- **Public hosting** - Is it on cloud/shared infrastructure?
- **Malicious IPs** - Does it resolve to known bad IPs?
- **ASN/Geolocation** - Where is it hosted?

**Example output:**
```json
{
  "tranco_rank": null,
  "in_crunchbase": false,
  "on_public_hosting": true,
  "resolves_to_malicious_ip": false,
  "reputation": "UNKNOWN - Not in top domains, on public hosting"
}
```

### 2. WHOIS Lookup (from L03.0)
**Source:** [../../l03_0_mcp_stdio/](../../l03_0_mcp_stdio/)

Provides:
- Domain registrar (e.g., MarkMonitor = brand protection)
- Registration date (new domains = higher risk)
- Registrant organization
- Name servers

**Security heuristic:**
- MarkMonitor/CSC registrar → Likely legitimate
- Registered days ago → High risk
- Privacy protection → Suspicious (but common)

### 3. VirusTotal Lookup (from L03.1)
**Source:** [../../l03_1_vt_mcp/](../../l03_1_vt_mcp/)
**Requires:** `VIRUSTOTAL_API_KEY`

Provides:
- How many security vendors flagged the domain
- Malware/phishing/spam categories
- Historical analysis
- Community votes

**Example:** `12/89 vendors flagged as phishing`

### 4. URLScan Analysis (from L03.2)
**Source:** [../../l03_2_urlscan_mcp/](../../l03_2_urlscan_mcp/)
**Requires:** `URLSCAN_API_KEY` (or use cached data)

Provides:
- Full-page screenshot
- Visual phishing indicators (fake logos, login forms)
- DOM tree analysis
- Network requests
- Technologies detected

**Multimodal analysis:** Gemini vision model analyzes screenshots for visual fraud

### 5. Threat Intelligence RAG (from L04)
**Source:** [../../l04_rag/](../../l04_rag/)

Provides:
- Historical context from security blogs
- Known attack campaigns (Kimsuky, Scattered Spider, etc.)
- TTPs (Tactics, Techniques, Procedures)
- IOCs (Indicators of Compromise)

**Example query:** "Tell me about phishing campaigns using fake PayPal sites"

## ReAct Planning Pattern

This agent uses **ReAct (Reasoning + Acting)**, a planning pattern where the agent:

1. **Reasons** about what information it needs
2. **Acts** by calling appropriate tools
3. **Observes** the results
4. **Reflects** on whether it has enough information
5. **Repeats** until confident in assessment

### Example ReAct Trace

```
User: "Is coinbase-arena.com safe?"

[Reasoning]
I need to assess this domain. Let me check:
1. Domain reputation
2. WHOIS information
3. Threat intelligence

[Acting - Tool Call 1]
domain_reputation("coinbase-arena.com")
→ Not in Tranco, not in Crunchbase, on public hosting

[Reasoning]
Suspicious. Let me check WHOIS for age and registrar.

[Acting - Tool Call 2]
whois_lookup("coinbase-arena.com")
→ Registered 3 days ago, privacy protection, unknown registrar

[Reasoning]
Very suspicious - new domain + typosquatting. Let me scan it.

[Acting - Tool Call 3]
urlscan_scan("coinbase-arena.com")
→ Screenshot shows fake Coinbase login form

[Final Assessment]
HIGH RISK - Phishing site impersonating Coinbase
Evidence:
- Domain registered 3 days ago
- Not legitimate Coinbase domain
- Fake login form in screenshot
- No reputation/business presence
```

## Agent Configuration

The agent is configured in [agent.py:1-108](agent.py#L1-L108):

```python
agent = Agent(
    model="gemini-2.5-pro",  # More capable model for complex reasoning
    tools=[
        domain_reputation,
        whois_lookup,
        virustotal_lookup,
        urlscan_scan,
        threat_intel_rag
    ],
    planner=BuiltInPlanner(thinking_budget=4096),  # ReAct planning enabled
    instructions="""
    You are an expert web security analyst...
    [Detailed instructions for tool usage and assessment criteria]
    """
)
```

### Why gemini-2.5-pro?

- **Better reasoning** - Handles complex multi-step analysis
- **Tool selection** - Chooses appropriate tools intelligently
- **Synthesis** - Combines evidence from multiple sources
- **Cost vs quality** - Worth the extra cost for security assessments

### Thinking Budget

`thinking_budget=4096` tokens allows the agent to:
- Reason through complex scenarios
- Plan multi-step tool calls
- Reflect on intermediate results
- Adjust strategy based on findings

**Too low (<1024):** Agent may rush to conclusions
**Too high (>8192):** Wastes tokens and costs more
**Sweet spot (4096):** Balanced reasoning depth

## Running the Agent

### Prerequisites

```bash
# Required
pip install google-adk google-genai

# For full functionality
pip install python-whois faiss-cpu sentence-transformers
```

### Environment Setup

**Minimum (use cached data):**
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

**Full functionality:**
```bash
GOOGLE_API_KEY=your_google_api_key_here
VIRUSTOTAL_API_KEY=your_vt_api_key_here
URLSCAN_API_KEY=your_urlscan_api_key_here
```

See [../../.env.example](../../.env.example) for template.

### Start the Agent

```bash
cd l06_web_sec_agent
adk web
```

Visit http://localhost:8080

### Example Queries

**Phishing detection:**
```
Is paypal-login.com a legitimate PayPal site?
Analyze coinbase-arena.com for phishing indicators
Should I trust reputationrescue.info?
```

**General assessment:**
```
Is google.com safe?  (should recognize as legitimate)
What can you tell me about example-suspicious-domain.com?
Investigate new-domain-here.com for security risks
```

**Threat intelligence:**
```
What do you know about Kimsuky APT?
Tell me about recent phishing campaigns
Are there any threats targeting financial institutions?
```

**Comprehensive analysis:**
```
Give me a full security assessment of suspicious-site.com including:
- Domain reputation
- WHOIS details
- Threat intelligence
- Visual analysis
- Final verdict
```

## Code Walkthrough

### agent.py - Main Agent

The capstone agent configuration with detailed instructions:

**Key sections:**

1. **Import MCP tools** from previous lessons
2. **Load custom domain reputation tool**
3. **Configure ReAct planner**
4. **Write comprehensive instructions** that:
   - Explain when to use each tool
   - Provide assessment criteria
   - Guide evidence synthesis
   - Specify output format

### tools/dominfo_server.py - Domain Reputation MCP

Custom MCP server that loads reputation data from [../../kb/](../../kb/):

```python
@mcp_server.tool()
def domain_reputation(domain: str):
    """Check domain reputation across multiple datasets"""
    kb = KnowledgeBase.get_instance()  # Singleton pattern

    return {
        "tranco_rank": kb.get_tranco_rank(domain),
        "in_crunchbase": kb.is_in_crunchbase(domain),
        "on_public_hosting": kb.is_public_hosting(domain),
        "resolves_to_malicious_ip": kb.check_malicious_ip(domain),
        "asn": kb.get_asn(domain),
        "geolocation": kb.get_location(domain)
    }
```

### tools/knowledgebase.py - Data Loader

Singleton class that loads ~96MB of reputation data:

```python
class KnowledgeBase:
    _instance = None

    def __init__(self):
        # Load once on first access
        self.tranco = self._load_tranco()          # 1M domains
        self.crunchbase = self._load_crunchbase()  # 3M domains
        self.malicious_ips = self._load_mal_ips() # 96K IPs
        # ... more datasets
```

**Why singleton?**
- Loads 96MB only once (not per request)
- ~2-5 second startup time
- ~150-200 MB memory usage
- O(1) lookup speed using sets/dicts

### tools/config.yml - Data Paths

Configuration file mapping dataset names to file paths:

```yaml
kb_paths:
  tranco: ../../kb/tranco.csv
  crunchbase: ../../kb/crunchbase.csv
  malicious_ips: ../../kb/mal_ips.csv
  # ... more datasets
```

## Decision Logic

The agent synthesizes information using these heuristics:

### HIGH RISK Indicators

- Domain registered <30 days ago
- Not in Tranco top 100K
- Resolves to known malicious IP
- VirusTotal: >5 vendors flag as malicious
- Screenshot shows fake login form
- Typosquatting known brand (e.g., paypal-login.com)

### MEDIUM RISK Indicators

- Not in Tranco or Crunchbase
- On public/shared hosting
- Privacy-protected WHOIS
- VirusTotal: 1-5 vendors suspicious
- Recently registered (30-90 days)

### LOW RISK Indicators

- In Tranco top 10K
- Reputable registrar (MarkMonitor, CSC)
- Registered >2 years ago
- In Crunchbase
- VirusTotal: Clean or 0-1 vendors flag
- Dedicated hosting infrastructure

### LEGITIMATE (High Confidence)

- Tranco top 1K
- Well-known organization
- Long registration history
- Multiple reputation signals align

## Performance Considerations

### Latency Breakdown

Typical query: "Is paypal-login.com safe?"

```
Domain Reputation: ~50ms   (local KB lookup)
WHOIS Lookup:      ~500ms  (network call)
VirusTotal:        ~300ms  (API call)
URLScan:           ~2s     (if cached) or ~60s (if new scan)
RAG Query:         ~200ms  (vector search + LLM)
Agent Reasoning:   ~3-5s   (LLM planning + synthesis)
───────────────────────────
Total:             ~6-8s   (with cache)
                   ~70s    (if URLScan not cached)
```

### Cost Breakdown

Per comprehensive assessment (all tools used):

```
Gemini 2.5-pro (reasoning):  ~$0.01-0.02  (4K thinking budget)
Vision model (screenshot):    ~$0.002     (if URLScan used)
RAG embeddings:               ~$0.0001    (if RAG queried)
VirusTotal API:               Free (4 req/min limit)
URLScan API:                  Free (50/day limit)
───────────────────────────────────────
Total per assessment:         ~$0.01-0.02
```

**For 1000 assessments/month:** ~$10-20

**Cost optimization:**
- Use gemini-2.0-flash for simpler queries (10x cheaper)
- Cache WHOIS/VT results (domains don't change often)
- Implement rate limiting to avoid waste
- Only call expensive tools when necessary

## Common Issues

**"Knowledge base loading takes too long"**
- First startup loads 96MB of data (~2-5 seconds)
- This is normal and only happens once
- Subsequent requests use cached data

**"Out of memory"**
- Knowledge base uses ~200MB RAM
- Ensure system has at least 512MB free
- For constrained environments, use a database instead

**"Agent doesn't call tools"**
- Check that instructions mention tool names
- Verify tools are loaded correctly (`adk web` shows available tools)
- Try more explicit queries ("Use WHOIS to check...")

**"VirusTotal/URLScan not working"**
- Verify API keys are set correctly
- Check rate limits (VT: 4/min, URLScan: 50/day)
- Use cached examples during workshop

**"Agent gives vague answers"**
- Increase thinking_budget (more reasoning tokens)
- Make instructions more specific
- Explicitly request evidence ("Show me the WHOIS data")

## Comparison with Previous Lessons

| Lesson | Complexity | Tools | Planning | Production-Ready |
|--------|------------|-------|----------|------------------|
| L01 | Low | 0 | No | Demo |
| L02 | Low | 1 | No | Demo |
| L03 | Medium | 1-2 | No | Component |
| L04 | Medium | 1 (RAG) | No | Component |
| L05 | Medium | 2-3 | Sequential/Parallel | Pattern |
| **L06** | **High** | **5** | **ReAct** | **Yes** |

## Production Deployment

To deploy this agent in production:

### 1. Infrastructure

```bash
# Use production-grade server
gunicorn -w 4 -b 0.0.0.0:8080 agent:app

# Add load balancer
# Add rate limiting
# Add caching layer (Redis)
```

### 2. Security

- Store API keys in secret manager (AWS Secrets Manager, GCP Secret Manager)
- Implement authentication (OAuth, API keys)
- Add input validation (prevent injection attacks)
- Rate limit per user/IP
- Log all assessments for audit trail

### 3. Monitoring

- Track tool call latency
- Monitor LLM token usage
- Alert on API failures
- Dashboard for assessment verdicts
- Cost tracking per query

### 4. Data Freshness

```bash
# Update knowledge base weekly
cron: "0 0 * * 0"  # Every Sunday
  - Download latest Tranco list
  - Update malicious IP feeds
  - Refresh GeoLite2 databases
  - Restart agent to reload data
```

### 5. Scaling

- Use async/await for I/O-bound operations
- Implement connection pooling for APIs
- Cache WHOIS/VT results in Redis
- Use CDN for static assets
- Consider serverless deployment (Cloud Run, Lambda)

## Next Steps

**You've completed the workshop!** 🎉

### Suggested Extensions

1. **Add more tools:**
   - Certificate transparency logs
   - DNS analysis (DNSSEC, CAA records)
   - Social media verification
   - Historical WHOIS data

2. **Improve decision logic:**
   - Machine learning for verdict classification
   - Bayesian reasoning for evidence weighting
   - Confidence scores instead of binary verdicts

3. **Enhance user experience:**
   - Generate PDF reports
   - Visualize evidence (charts, graphs)
   - Explain reasoning traces
   - Provide remediation recommendations

4. **Scale to production:**
   - Implement batch processing
   - Add webhook notifications
   - Build REST API
   - Create Slack/Teams integration

## Additional Resources

- [Google ADK Documentation](https://google.github.io/adk/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629) - Original research
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Workshop Presentation](../../building_web_security_agents.pdf)
- [Demo Video](../../web_sec_agent_demo.mp4)

## Acknowledgments

This capstone brings together:
- **L01:** Agent fundamentals
- **L02:** Custom tool creation
- **L03:** MCP architecture
- **L04:** RAG knowledge grounding
- **L05:** Multi-agent patterns
- **L06:** Production integration

Thank you for completing the Web Security Agents workshop!
