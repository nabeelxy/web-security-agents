from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

toolset = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url = "http://127.0.0.1:8001/mcp"
        )

    )

root_agent = LlmAgent(
    name="agent_01_adk",
    model="gemini-2.0-flash",
    description="""
        Web security analyst. 
        """,
    instruction="""
        You are an expert web security analysis agent.
        You may use the get_domain_whois tool
        to learn the WHOIS record for the domain which takes
        a domain name such as google.com or meta.com as an input. 
        If the registrar of the domain is MarkMonitor or SPC, 
        the domain is likely to be a 
        brand protected. Further, domain organization or registrant
        is a reputed organization, the domain is likely to be benign.
        """,
    tools=[toolset]
)
