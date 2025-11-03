from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
import os

server_path = os.path.join(os.path.dirname(__file__), "server.py")
toolset_urlscan = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [server_path]
            },
            timeout=120
        )

    )

root_agent = LlmAgent(
    name="agent_03_mcp_urlscan",
    model="gemini-2.0-flash",
    description="""
        Web security analyst. 
        """,
    instruction="""
        You are an expert web security analysis agent.
        You may use the UrlScan MCP tool
        to learn to fetch the UrlScan report
        for a domain or URL. VirusTotal report contains information
	about the crawling results of a website including technologies
	used, resolutions, web traffic and more. 
        """,
    tools=[toolset_urlscan]
)
