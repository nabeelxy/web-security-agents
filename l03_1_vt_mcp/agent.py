from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
import os

server_path = os.path.join(os.path.dirname(__file__), "server.py")
toolset_vt = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [server_path]
            },
            timeout=120
        )

    )

root_agent = LlmAgent(
    name="agent_03_vt_mcp",
    model="gemini-2.0-flash",
    description="""
        Web security analyst. 
        """,
    instruction="""
        You are an expert web security analysis agent.
        You may use the VirusTotal MCP tool
        to learn to fetch the VirusTotal report
        for a domain or URL. VirusTotal report contains 90 odd
        web scanners that identify a given url/domain as phishing, 
        malicious, suspicious or benign. Some scanners may say
        unknown. Usually, if 2 to 4 scanners mentions that the
        domain/url is malicious/phishing, then the domain/url has
        some possiblity to be malicious. if more than 5 scanners 
        mentions the url/domain is malicious/phishing, the domain/url
        is highly likely to be malicious. 
        """,
    tools=[toolset_vt]
)
