from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from google.adk.tools import google_search
import os

whois_server_path = os.path.join(os.path.dirname(__file__), "../l03_0_mcp_stdio/server.py")
toolset_whois = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [whois_server_path]
            },
            timeout=120
        )
    )

urlscan_server_path = os.path.join(os.path.dirname(__file__), "../l03_2_urlscan_mcp/server.py")
toolset_urlscan = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [urlscan_server_path]
            },
            timeout=120
        )
    )

vt_server_path = os.path.join(os.path.dirname(__file__), "../l03_1_vt_mcp/server.py")
toolset_vt = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [vt_server_path]
            },
            timeout=120
        )
    )

dominfo_server_path = os.path.join(os.path.dirname(__file__), "tools/dominfo_server.py")
toolset_dominfo = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [dominfo_server_path]
            },
            timeout=120
        )
    )

threatintel_server_path = os.path.join(os.path.dirname(__file__), "../l04_rag/server.py")
toolset_threatintel = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params= {
                "command" : "python" ,
                "args" : [threatintel_server_path]
            },
            timeout=120
        )
    )

root_agent = LlmAgent(
    name="web_security_agent",
    model="gemini-2.5-pro",
    description="Web security analyst.",
    instruction="""
        You are an expert web security analysis agent.
        Your goal is to conduct systematic, comprehensive web security investigation.
        You may use various tools provided to answer the question asked.

        Depending the question asked, first decide which tools to use and in which sequence.
        You may decided the tool invocation sequency dynamically through the reason-action 
        loop and use the optimal tools to solve the problem at hand.

        In general, when analyzing a domain or URL, follow these key investigation steps:

        1. Initial Domain Intelligence
        - Retrieve domain registration details
        - Check domain age and historical ownership
        - Identify registrar and name servers
        - Examine domain location and registrant information
        - Analyze potential geopolitical or legal risks
        - Use domain reputation and threat intelligence tools
        2. Check domain/URL scan results
        - Perform VirusTotal scans - if 1 or 2 scanners say it is malicious/phishing, it is a
          suspicious domain/url, if 2 to 4 scanners say it is malicious/phishing, it is medium confidence
          threat and if more than 5 scanners say malicious, it is high confidence threat.
          VirusTotal reports can have false positives and therefore check domain reputation and other
          information before making conclusive judgements.
        - Perform UrlScan screenshot analysis
        3. Use Google search to analyze web reputation and any information available
        - Check web ranking, references, and potential security reviews
        - Look for news articles, forum discussions about domain/URL
        4. Use the threat intelligence tool to assess if it is already discussed in reputed
        threat intel databases
        - This tool has global threat database and reports from trusted security platforms
        - You can treat the threat intel information with high confidence
        """,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=4096,
        )
    ),

    tools=[toolset_whois, toolset_dominfo, toolset_urlscan, toolset_vt, toolset_threatintel, google_search]
)
