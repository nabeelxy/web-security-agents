from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
import os

server_path = os.path.join(os.path.dirname(__file__), "server.py")
toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [server_path]
            }
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
