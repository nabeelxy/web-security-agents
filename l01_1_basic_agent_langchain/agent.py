from langchain.agents import create_agent

agent = create_agent(
    model="gemini-2.0-flash",
    system_prompt="You are an expert web security analysis agent.",
)

# Run the agent
output1 = agent.invoke(
    {"messages": [{"role": "user", "content": "Is paypal.com benign?"}]}
)

print(output1)

# Run agent again
output2 = agent.invoke(
    {"messages": [{"role": "user", "content": "Is paypal-login.com benign?"}]}
)

print(output2)
