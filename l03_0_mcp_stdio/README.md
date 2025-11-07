# Model Context Protocol
This example shows how to wrap the whois tool we built in the previous lesson into a MCP tool. We use the awesome mcp Python library to make this a breeze.

MCP supports three types of endpoints:
- Tools
- Resources
- Prompts

In this lesson, we focus on the tools.

MCP supports three transport options.
- Stdio (for local testing)
- Sse (deprecated)
- Streamable HTTP (preferred method for remote hosting)

This lesson shows how to use the Stdio transport. Stdio transport is a great way to test your server before you deploy it remotely.
