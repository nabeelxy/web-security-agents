# Web Security Agents

A hands-on workshop for building LLM-powered agents to automate web security investigations. This repository walks you through progressively building a production-ready security agent using Google ADK (Agent Development Kit), covering fundamental concepts like in-context learning, tool calling, MCP servers, RAG, multi-agent orchestration, and ReAct planning.

## Workshop Overview

**Duration:** ~2 hours

**Target Audience:** Security professionals and developers interested in AI-powered automation

**Primary Framework:** Google ADK (with LangChain and Ollama alternatives shown)

**Note:** This repo is originally made for the [eCrime 2025](https://apwg.org/events/ecrime2025) in San Diego in Nov 2025 and extended with additional details.


### What You'll Build

By the end of this workshop, you'll create a comprehensive web security agent that:
- Performs domain reputation analysis using multiple threat intelligence sources
- Conducts WHOIS lookups and certificate analysis
- Analyzes website screenshots using vision models
- Retrieves historical threat intelligence through RAG
- Provides comprehensive security assessments with reasoning traces

### Learning Objectives

- Understand LLM agent architectures and when to use them
- Implement tool calling for extending agent capabilities
- Build modular, reusable tools using Model Context Protocol (MCP)
- Ground agent responses in domain knowledge using RAG
- Orchestrate multiple agents for complex workflows
- Design production-ready ReAct agents with planning capabilities

## Prerequisites

### Required

- **Python 3.10+** (tested on 3.10, 3.11, 3.12)
- **Google Cloud Account** with Gemini API access
- **API Keys** (some lessons require these):
  - Google AI API key (get from [Google AI Studio](https://aistudio.google.com/apikey))
  - VirusTotal API key (optional, for L03.1 - get from [VirusTotal](https://www.virustotal.com/gui/join-us))
  - URLScan.io API key (optional, for L03.2 - get from [URLScan.io](https://urlscan.io/))

### Optional

- **Docker** (for Ollama local models in L01.2)
- **Git** (for cloning the repository)

### Knowledge Prerequisites

- Basic Python programming
- Familiarity with APIs and JSON
- Understanding of web security concepts (helpful but not required)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nabeelxy/web-security-agents.git
cd web-security-agents
```

### 2. Install Dependencies

```bash
pip install google-adk google-genai langchain langchain-google-genai
pip install python-whois faiss-cpu sentence-transformers
```

### 3. Configure API Keys

Create a `.env` file in the root directory (or set environment variables):

```bash
# Required for all lessons
GOOGLE_API_KEY=your_google_api_key_here

# Optional - for specific lessons
VIRUSTOTAL_API_KEY=your_vt_api_key_here
URLSCAN_API_KEY=your_urlscan_api_key_here
```

See [.env.example](.env.example) for a complete template.

### 4. Verify Installation

```bash
# Test basic agent (requires GOOGLE_API_KEY)
cd l01_0_basic_agent_adk
adk web
```

Visit http://localhost:8080 and ask the agent a question. If it responds, you're ready to go!

## Workshop Structure

The workshop is organized into 7 progressive lessons, each building on the previous:

### Lesson 1: Basic Agents (30 min)

**Concepts:** In-context learning, agent frameworks, deployment modes

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l01_0_basic_agent_adk](l01_0_basic_agent_adk/) | Simplest possible ADK agent | Agent creation, web UI |
| [l01_1_basic_agent_langchain](l01_1_basic_agent_langchain/) | LangChain alternative | Framework comparison |
| [l01_2_basic_agent_ollama](l01_2_basic_agent_ollama/) | Local model deployment | Privacy, cost control |
| [l01_3_basic_agent_no_web](l01_3_basic_agent_no_web/) | Programmatic usage | API integration |

**What you'll learn:** How to create basic agents, choose frameworks, and deploy in different modes.

### Lesson 2: Tool Calling (20 min)

**Concepts:** Function calling, tool schemas, custom tools

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l02_0_tool_calling_adk](l02_0_tool_calling_adk/) | Built-in Google Search tool | Using pre-built tools |
| [l02_1_tool_calling_adk](l02_1_tool_calling_adk/) | Custom WHOIS tool | Creating custom tools |
| [l02_2_tool_calling_langchain](l02_2_tool_calling_langchain/) | LangChain tool implementation | Framework differences |

**What you'll learn:** How to extend agent capabilities with function calling and custom tools.

### Lesson 3: MCP Servers (25 min)

**Concepts:** Model Context Protocol, transport layers, API integration

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l03_0_mcp_stdio](l03_0_mcp_stdio/) | STDIO transport (local testing) | MCP basics, server/client |
| [l03_0_mcp_http](l03_0_mcp_http/) | HTTP transport (remote hosting) | Network transport |
| [l03_1_vt_mcp](l03_1_vt_mcp/) | VirusTotal integration | Real-world APIs |
| [l03_2_urlscan_mcp](l03_2_urlscan_mcp/) | URLScan with screenshot analysis | Multimodal, caching |

**What you'll learn:** How to build modular, reusable tool servers using the MCP standard.

### Lesson 4: RAG (15 min)

**Concepts:** Vector embeddings, semantic search, knowledge grounding

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l04_rag](l04_rag/) | FAISS-based threat intelligence RAG | Vector databases, retrieval |
| [l04_1_rag_file_tool](l04_1_rag_file_tool/) | Google File Search alternative | Managed alternatives |

**What you'll learn:** How to ground agent responses in domain-specific knowledge using RAG.

### Lesson 5: Multi-Agent Orchestration (15 min)

**Concepts:** Workflow patterns, agent composition

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l05_multi_agent_sequential](l05_multi_agent_sequential/) | Pipeline pattern (NS → ASN) | Sequential workflows |
| [l05_multi_agent_parallel](l05_multi_agent_parallel/) | Fan-out/fan-in pattern | Parallel execution |
| [l05_multi_agent_loop](l05_multi_agent_loop/) | Iterative refinement | Loop patterns |

**What you'll learn:** How to orchestrate multiple agents for complex workflows.

### Lesson 6: Capstone - ReAct Agent (15 min)

**Concepts:** ReAct planning, comprehensive integration

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l06_web_sec_agent](l06_web_sec_agent/) | Production security agent | Combining all concepts |

**What you'll learn:** How to build a production-ready agent that combines all previous lessons.

### Lesson 7: Agent Evaluations (20 min)

**Concepts:** Evaluation datasets, metrics, quality assurance

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l07_0_agent_evals_basic](l07_0_agent_evals_basic/) | Build eval datasets and measure agent quality | Testing and validation |

**What you'll learn:** How to create evaluation datasets, run automated tests, and measure agent performance.

## Key Concepts

### In-Context Learning
LLMs can follow instructions and reason about problems without explicit tool use. Basic agents demonstrate pure reasoning capabilities.

### Tool Calling (Function Calling)
Agents can invoke external functions/APIs by generating structured JSON that maps to tool schemas. This extends agent capabilities beyond the LLM's knowledge cutoff.

### Model Context Protocol (MCP)
A standardized protocol for building reusable tool servers that can be shared across different agent frameworks. Think of it as a "USB standard" for AI tools.

### Retrieval Augmented Generation (RAG)
Technique for grounding agent responses in external knowledge by retrieving relevant documents and including them in the context window.

### Multi-Agent Systems
Orchestrating multiple specialized agents to solve complex problems through sequential, parallel, or iterative workflows.

### ReAct (Reasoning + Acting)
An agent planning pattern that interleaves reasoning traces with tool calls, allowing agents to plan, execute, and adapt their approach.

## Data Files

This repository includes pre-processed data files to accelerate the workshop:

- **[kb/](kb/)** - Domain reputation knowledge bases (~96MB)
  - Tranco top domains, Crunchbase business domains, malicious IPs, geolocation data
- **[data/](data/)** - Cached URLScan results and screenshots
  - Pre-fetched scans to avoid rate limiting during the workshop
- **[l04_rag/](l04_rag/)** - Threat intelligence reports and pre-computed FAISS index
  - 5 real-world threat reports, embedded and ready for semantic search

See individual README files in each directory for details.

## Workshop Flow

**Recommended Path:**

1. **Start with L01.0** - Get the basic agent working to validate your setup
2. **Skim L01.1-L01.3** - Understand alternatives but don't spend too much time
3. **Focus on L02.1** - Custom tool creation is critical
4. **Deep dive into L03** - MCP is the key architectural pattern
5. **Understand L04** - RAG concepts apply beyond this workshop
6. **Quick review of L05** - See the patterns, don't implement from scratch
7. **Explore L06** - See how everything comes together
8. **Practice L07** - Learn to evaluate and validate agent quality

**Time Management:**
- Don't try to run every example
- Focus on understanding patterns over syntax
- Use the capstone (L06) as your reference for "how it all fits together"

## Troubleshooting

### Common Issues

**"API key not found"**
- Ensure `.env` file exists in the root directory
- Check that `GOOGLE_API_KEY` is set correctly
- For programmatic usage, ensure environment variables are loaded

**"adk: command not found"**
- Run `pip install google-adk`
- Verify installation: `adk --version`

**"Rate limit exceeded" (VirusTotal, URLScan)**
- Free tier APIs have strict rate limits
- Use the cached data in `data/` folder
- Consider upgrading to paid tiers for production use

**"FAISS index not found"**
- The pre-computed index is included in the repo
- If missing, run `python create_vector_db.py` in [l04_rag/](l04_rag/)

**"Import errors" (faiss, sentence-transformers)**
- Install missing dependencies: `pip install faiss-cpu sentence-transformers`

## Production Considerations

This workshop demonstrates core concepts with working code. For production deployment:

- Implement proper error handling and retry logic
- Add rate limiting and request throttling
- Use async/await for I/O-bound operations
- Implement proper logging and monitoring
- Secure API keys using secret management services
- Add input validation and sanitization
- Consider costs of LLM API calls and optimize prompts
- Implement caching strategies for expensive operations
- Test thoroughly with adversarial inputs

## Additional Resources

- **Google ADK Documentation:** https://google.github.io/adk/
- **Model Context Protocol Spec:** https://spec.modelcontextprotocol.io/
- **LangChain Documentation:** https://python.langchain.com/
- **Gemini API Documentation:** https://ai.google.dev/docs
- **Workshop Presentation:** [building_web_security_agents.pdf](building_web_security_agents.pdf)
- **Demo Video:** [web_sec_agent_demo.mp4](web_sec_agent_demo.mp4)

## Contributing

Found an issue or want to improve the workshop? Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Submit a pull request

## License

This workshop material is provided as-is for educational purposes.

## Acknowledgments

- WHOIS lookup implementation adapted from [dnstwist](https://github.com/elceef/dnstwist)
- Threat intelligence reports sourced from public security blogs
- Domain reputation data from Tranco, Crunchbase, and threat feeds
