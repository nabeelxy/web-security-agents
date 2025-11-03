from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    name="agent_01_adk",
    model=LiteLlm(model="ollama/gemma3:4b"), #gpt-oss:20b
    description="Web security analyst.",
    instruction="You are an expert web security analysis agent."
)