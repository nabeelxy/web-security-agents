# Web Security Agent

This the capstone project where we bring all our leanings into one agent. Specifically, in this lesson, we combine all tools together to build a comprehensive web security agent that can assess any URL. 


Note that additional tools we build are placed under tools folder.

## Tools used
- VT MCP tool (lesson 3) - VirusTotal intelligence on the URL
- WHOIS MCP tool (lesson 3) - Domain whois information
- UrlScan MCP tool (lesson 3) - URL scanning intelligenc
- Threat Intel RAG tool (lesson 4) - knowledge from reputed blog posts
- Reputation MCP tool (lesson 6, i.e. this lesson) - Domain reputation information such as Tranco rank, Presence in Crunchbase, and so on

## Agent Planning
We use a ReAct (reasoning and acting) agentic pattern to answer the queries raised.

## Runing the agent
```
adk web
```
