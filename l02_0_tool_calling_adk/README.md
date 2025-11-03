# Agent with a built-in tool
The goal is to create a  agent using Google ADK and provide
access to google_search tool to perform Google searches.


## Getting the API key
In order to use Google ADK, we need an API key. Go to aistudio.google.com and create your key.

Copy the following to .env file:
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<your-api-key>

Run the agent:
cd ..
adk web
Open http://127.0.0.1:8000 in your favorite browser

Example Queries to try:
Is paypal.com benign?
Is paypal-login.com benign?

