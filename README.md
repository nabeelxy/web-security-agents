# Web Security Agents

This repo is for people in a hurry to get to know how to use LLM agents (mainly through Google ADK) to automate web security investigation. It walks you through key concepts of in-context learning, tool calling, MCP, RAG, Multi-Agents and ReAct Agent planning using easy to run code snippets.


## Getting started

```
cd existing_repo
git remote add origin https://github.com/nabeelxy/web-security-agents.git
git branch -M main
git push -uf origin main
```

## Basic Agents
- A basic agent using ADK
- A basic agent using LangChain
- A basic agent using ollama
- A basic agent using ADK but can run standalone without adk web

## Agents with Tools
- Built-in tool calling with ADK
- Custom tool calling with ADK
- Custom tool calling with LangChain

## Agents with MCP Servers
- A basic MCP server with stdio transport
- A basic MCP server with http transport
- A MCP server for VT APIs (threat intelligence)
- A MCP server for UrlScan APIs (web page crawling)

## Agents with RAG
- Threat intelligence RAG agent

## Multi-Agents
- Sequential agent
- Parallel agent
- Loop agent


## Web Security Agent
- A ReAct Agent (i.e. an Agent in a Loop iteratively using tools) to investigate websites
