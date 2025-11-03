from google.adk.agents import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="agent_02_adk_tool",
    model="gemini-2.0-flash",
    description="""
        Web security analyst. 
        """,
    instruction="""
        You are an expert web security analysis agent.
        You may use the google_search tool to retrieve
        information about the query to answer the analysis
        question.
        """,
    tools=[google_search]
)