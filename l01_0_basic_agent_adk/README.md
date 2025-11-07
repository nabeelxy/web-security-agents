# First Basic Agent
The goal is to create a very simple agent using Google ADK and then use adk web.

There are in fact 4 ways to run an agent:
- CLI (adk run)
- Web UI (adk web)
- API Server (adk api_server)
- API (Python)

For initial development adk web is an excellent environment as it provides session memory and tracing out of the box. Once you have validated your implementation, you may want to use the API to make it hands off.

## Getting the API key
In order to use Google ADK with your personal account, we need an API key. Go to aistudio.google.com and create your key.

If you are an enterprise user, you may obtain a service key and set the environment variables mentioned below.

### System:
```
python3 -m venv ./wsa_env
source ./wsa_env/bin/activate
pip install -r requirements.txt
```

### Copy the following to .env file:

For the personal account:
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=<your-api-key>
```

For the enterprise account:
```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=<project-name>
GOOGLE_CLOUD_LOCATION=<location>
```

### Run the agent:
```
cd ..
adk web
Open http://127.0.0.1:8000 in your favorite browser
```

### Example Queries to try:
- Is paypal.com benign?
- Is paypal-login.com benign?

