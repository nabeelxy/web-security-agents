from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "basic_agent_no_web"
USER_ID = "user_1"
SESSION_ID = "session_1"

async def get_agent():
    root_agent = LlmAgent(
       name="agent_01_adk",
       model="gemini-2.0-flash",
       description="Web security analyst.",
       instruction="You are an expert web security analysis agent."
    )
    return root_agent

# step 2 : run the agent
async def run_agent(query):

    # create memory session 
    session_serivce = InMemorySessionService()
    await session_serivce.create_session(app_name= APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    
    # get the agent 
    root_agent = await get_agent()

    # create runnner instance
    runner = Runner(app_name=APP_NAME, agent = root_agent, session_service=session_serivce)

    # format the query 
    content = types.Content(role = "user", parts= [types.Part(text=query)])

    print("Running agent with query:", query)
    # run the agent 
    events = runner.run_async (
        new_message = content,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )


    # print the response
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)


if __name__ == "__main__":
    asyncio.run(run_agent("Is paypal.com benign?"))

