# Web Security Agents

A hands-on workshop for building LLM-powered agents to automate web security investigations. This repository walks you through progressively building a production-ready security agent using Google ADK (Agent Development Kit), covering fundamental concepts like in-context learning, tool calling, MCP servers, RAG, multi-agent orchestration, and ReAct planning.

## Workshop Overview

**Duration:** ~8-9 hours total (L01-L09: ~2 hours, L10-L21: ~6-7 hours)

**Target Audience:** Security professionals and developers interested in AI-powered automation

**Primary Framework:** Google ADK (with LangChain and Ollama alternatives shown)

**Note:** This repo is originally made for the [eCrime 2025](https://apwg.org/events/ecrime2025) in San Diego in Nov 2025 and extended with additional details and lessons.


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

The workshop is organized into 21 progressive lessons, each building on the previous:

### Lesson 1: Basic Agents (30 min)

**Concepts:** In-context learning, agent frameworks, deployment modes

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l01_0_basic_agent_adk](l01_0_basic_agent_adk/) | Simplest possible ADK agent | Agent creation, web UI |
| [l01_1_basic_agent_langchain](l01_1_basic_agent_langchain/) | LangChain alternative | Framework comparison |
| [l01_2_basic_agent_ollama](l01_2_basic_agent_ollama/) | Local model deployment | Privacy, cost control |
| [l01_3_basic_agent_no_web](l01_3_basic_agent_no_web/) | Programmatic usage | API integration |

**What you'll learn:** How to create basic agents, choose frameworks, and deploy in different modes.

**💡 Recommended:** After completing L01, jump to [Lesson 9: Prompt Engineering](l09_prompt_engineering/) to learn how to craft effective prompts. This foundational skill will improve all subsequent lessons.

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

### Lesson 8: Observability and Tracing (15 min)

**Concepts:** Distributed tracing, performance monitoring, debugging

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l08_0_agent_observability](l08_0_agent_observability/) | Trace agent execution and analyze performance | Production monitoring |

**What you'll learn:** How to instrument agents with tracing, identify bottlenecks, and build observability for production.

### Lesson 9: Prompt Engineering (20 min)

**Concepts:** System prompts, few-shot learning, chain-of-thought, structured output

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l09_prompt_engineering](l09_prompt_engineering/) | Craft effective prompts through examples and iteration | Prompt optimization |

**What you'll learn:** How to write system prompts, use few-shot examples, apply chain-of-thought reasoning, create templates, and debug poor outputs.

**⭐ Foundation Lesson:** This lesson is best taken right after L01 as good prompting is critical for all agent development.

### Lesson 10: Safety & Content Filtering (25 min)

**Concepts:** Defense-in-depth, prompt injection detection, input validation, output filtering

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l10_safety_filtering](l10_safety_filtering/) | 5-layer security architecture | Input validation, injection detection, rate limiting |

**What you'll learn:** How to protect agents from prompt injection attacks, validate inputs, filter outputs, and implement rate limiting.

### Lesson 11: Error Handling & Resilience (25 min)

**Concepts:** Retry logic, circuit breakers, fallback strategies

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l11_error_handling](l11_error_handling/) | Resilient agent with error recovery | Exponential backoff, graceful degradation |

**What you'll learn:** How to handle API failures, implement retry logic with exponential backoff, use circuit breakers, and design multi-tier fallback strategies.

### Lesson 12: Cost Optimization & Caching (30 min)

**Concepts:** Exact caching, semantic caching, cost tracking

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l12_cost_optimization](l12_cost_optimization/) | Reduce costs by 80%+ with caching | Multi-tier caching, cost monitoring |

**What you'll learn:** How to implement exact and semantic caching, track token usage and costs, and optimize LLM API spend.

### Lesson 13: Human-in-the-Loop (30 min)

**Concepts:** Confidence scoring, approval workflows, audit trails

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l13_human_in_the_loop](l13_human_in_the_loop/) | Balance automation with human oversight | Review queues, confidence thresholds |

**What you'll learn:** How to calculate confidence scores, route low-confidence decisions to humans, manage review queues, and create audit trails.

### Lesson 14: Streaming & Async (25 min)

**Concepts:** Streaming responses, Server-Sent Events, parallel execution

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l14_streaming](l14_streaming/) | Progressive disclosure and async operations | SSE, AsyncIterator, parallelization |

**What you'll learn:** How to stream agent responses for better UX, implement Server-Sent Events, and parallelize tool execution for 2-3x speedup.

### Lesson 15: Memory & State Management (20 min)

**Concepts:** Conversation memory, context window management, summarization

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l15_memory](l15_memory/) | Multi-turn conversations with memory | Message history, context limits |

**What you'll learn:** How to maintain conversation context, manage token limits, and implement automatic summarization.

### Lesson 16: Production Deployment (35 min)

**Concepts:** Docker, Kubernetes, health checks, scalability

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l16_production](l16_production/) | Deploy to production with Docker & Kubernetes | Containerization, orchestration, monitoring |

**What you'll learn:** How to containerize agents with Docker, orchestrate services with docker-compose, deploy to Kubernetes, and implement production best practices.

### Lesson 17: Advanced RAG (40 min)

**Concepts:** Advanced chunking, hybrid search, vector databases, retrieval optimization

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l17_advanced_rag](l17_advanced_rag/) | 2-3x better RAG with advanced techniques | Recursive chunking, MMR, reranking, HyDE |

**What you'll learn:** How to improve RAG quality with advanced chunking strategies (recursive, semantic, parent-child), hybrid search (dense + sparse), cross-encoder reranking, MMR for diversity, and production vector database choices (FAISS, Chroma, Qdrant, Pinecone).

### Lesson 18: Vision & Multimodal Agents (35 min)

**Concepts:** Gemini Vision API, multimodal reasoning, image analysis, visual security threats

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l18_vision_multimodal](l18_vision_multimodal/) | Analyze screenshots, detect phishing, extract IOCs from images | Vision capabilities, cross-modal validation |

**What you'll learn:** How to use Gemini Vision for analyzing security screenshots, detecting phishing from images, extracting IOCs with OCR, analyzing malware UIs, interpreting threat intel charts, and combining text + images for cross-modal validation.

### Lesson 19: Agent Routing & Conditional Logic (30 min)

**Concepts:** Intent classification, specialized agents, load balancing, conditional routing

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l19_agent_routing](l19_agent_routing/) | Route queries to specialized agents for 40-60% better accuracy | LLM/rule-based classification, routing strategies |

**What you'll learn:** How to classify user intents (LLM-based, rule-based, hybrid), route queries to specialized agents, implement load balancing, multi-agent consultation, and context-aware routing for optimal results.

### Lesson 20: Testing & Quality Assurance (40 min)

**Concepts:** Test frameworks, synthetic data, evaluation metrics, A/B testing, edge cases

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l20_testing_qa](l20_testing_qa/) | Comprehensive testing for production-ready agents | Unit/workflow tests, metrics, regression testing |

**What you'll learn:** How to build test frameworks for agents, generate synthetic test data with LLMs, measure performance with evaluation metrics (accuracy, precision, recall, F1), A/B test agent versions, test edge cases, and implement regression testing.

### Lesson 21: Advanced Web Security Agent (30 min)

**Concepts:** Production-ready agent, security hardening, reliability, cost optimization

| Example | Description | Key Learning |
|---------|-------------|--------------|
| [l21_advanced_web_sec_agent](l21_advanced_web_sec_agent/) | L06 enhanced with L10-L13 production features | Security, resilience, caching, human review, observability |

**What you'll learn:** How to transform L06's basic agent into a production-ready system by adding input validation (L10), error handling (L11), caching (L12), human-in-the-loop (L13), and observability (L08). Focus on security-first design and robust, reliable web security analysis.

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

**Part 1: Core Agent Development (L01-L09)**
1. **Start with L01.0** - Get the basic agent working to validate your setup
2. **⭐ Jump to L09** - Learn prompt engineering (foundational skill for everything else)
3. **Skim L01.1-L01.3** - Understand alternatives but don't spend too much time
4. **Focus on L02.1** - Custom tool creation is critical
5. **Deep dive into L03** - MCP is the key architectural pattern
6. **Understand L04** - RAG concepts apply beyond this workshop
7. **Quick review of L05** - See the patterns, don't implement from scratch
8. **Explore L06** - See how everything comes together
9. **Practice L07** - Learn to evaluate and validate agent quality
10. **Study L08** - Understand production observability and monitoring

**Part 2: Production-Ready Features (L10-L21)**
11. **Security first: L10** - Protect against prompt injection and attacks
12. **Build resilience: L11** - Handle failures gracefully with retry logic
13. **Optimize costs: L12** - Implement caching to reduce LLM API costs by 80%+
14. **Add oversight: L13** - Balance automation with human review
15. **Improve UX: L14** - Stream responses and parallelize operations
16. **Maintain context: L15** - Handle multi-turn conversations
17. **Deploy to prod: L16** - Containerize and deploy with Docker/Kubernetes
18. **Advanced RAG: L17** - Improve RAG quality 2-3x with advanced techniques
19. **Add vision: L18** - Analyze screenshots and images for visual threats
20. **Implement routing: L19** - Route queries to specialized agents for better results
21. **Test thoroughly: L20** - Build comprehensive test suites for production confidence
22. **⭐ L21: Production Agent** - See L06 enhanced with L10-L13 security and reliability features

**Time Management:**
- L01-L09 can be completed in ~2 hours for core concepts
- L10-L21 adds ~6-7 hours for production readiness
- Don't try to run every example - understand patterns over syntax
- Use L06 as your reference for "how it all fits together"
- Use L16 to see how to deploy everything to production
- Use L17 to optimize RAG quality after building basic RAG in L04
- Use L18 for multimodal security analysis with vision
- Use L19 for intelligent query routing to specialized agents
- Use L20 to build comprehensive test coverage before deployment
- **Use L21 to see L06 transformed into a production-ready secure agent**

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

This workshop demonstrates core concepts with working code. **Lessons 10-16 specifically address production readiness:**

**Security & Safety (L10):**
- Input validation and sanitization
- Prompt injection detection (OWASP #1 LLM vulnerability)
- Output filtering for PII and harmful content
- Rate limiting and abuse prevention

**Reliability & Resilience (L11):**
- Error handling with retry logic and exponential backoff
- Circuit breakers for external services
- Multi-tier fallback strategies
- Graceful degradation

**Cost Optimization (L12):**
- Exact and semantic caching (80%+ cost reduction)
- Token usage tracking and monitoring
- Multi-tier caching strategies
- Cost per request metrics

**Quality & Oversight (L13):**
- Confidence scoring for automated decisions
- Human-in-the-loop review workflows
- Audit trails for compliance
- Continuous learning from human feedback

**Performance & UX (L14):**
- Streaming responses for progressive disclosure
- Parallel tool execution (2-3x speedup)
- Server-Sent Events (SSE) for web clients
- Async/await patterns

**State Management (L15):**
- Conversation memory and context management
- Token limit handling
- Automatic summarization

**Deployment (L16):**
- Docker containerization
- Kubernetes orchestration
- Health checks and monitoring
- Secrets management
- Zero-downtime deployments
- Auto-scaling

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

## Citation

If you use any lessons from this in your research or project, please cite:

```bibtex
@misc{ecrime2025agents,
  title = {How to Build Agentic Systems to Automate Web Security},
  booktitle = {eCrime 2025},
  author = {Mohamed Nabeel},
  year = {2025},
  url = {https://github.com/nabeelxy/web-security-agents}
}
```

## Acknowledgments

- WHOIS lookup implementation adapted from [dnstwist](https://github.com/elceef/dnstwist)
- Threat intelligence reports sourced from public security blogs
- Domain reputation data from Tranco, Crunchbase, and threat feeds
