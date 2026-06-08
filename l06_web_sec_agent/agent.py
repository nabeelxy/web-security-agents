from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset
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

skills_dir = os.path.join(os.path.dirname(__file__), "skills/domain-assessment")
skill_toolset = SkillToolset(skills=[load_skill_from_dir(skills_dir)])

root_agent = LlmAgent(
    name="web_security_agent",
    model="gemini-2.5-pro",
    description="Web security analyst.",
    instruction="You are an expert web security analysis agent. Use your available skills to handle user requests.",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=4096,
        )
    ),
    tools=[skill_toolset, toolset_whois, toolset_dominfo, toolset_urlscan, toolset_vt, toolset_threatintel]
)
