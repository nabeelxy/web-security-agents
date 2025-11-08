# Web Security Agent

In this lesson, we combine all tools together to build a comprehensive web security agent that can assess any URL. Additional tools we build are placed under tools folder.

## Tools used
- VT MCP tool - VirusTotal intelligence on the URL
- WHOIS MCP tool - Domain whois information
- UrlScan MCP tool - URL scanning intelligenc
- Threat Intel RAG tool - knowledge from reputed blog posts
- Reputation MCP tool - Domain reputation information such as Tranco rank, Presence in Crunchbase, and so on

## Agent Planning
We use a ReAct (reasoning and acting) agentic pattern to answer the queries raised.

## Runing the agent
```
adk web
```
