from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="agent_01_adk",
    model="gemini-2.0-flash",
    description="Web security analyst.",
    instruction="You are an expert web security analysis agent."
)