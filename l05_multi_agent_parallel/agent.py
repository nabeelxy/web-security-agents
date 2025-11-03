from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search

def whois_tool(domain: str) -> dict:
    """
    Fetch WHOIS information for a given domain.

    Args:
        domain (str): Domain name to lookup

    Returns:
        dict: WHOIS record details
    """
    return {
        "registrar": "MarkMonitor",
        "creation_date": "2023-01-15",
        "registrant_org": "Example Corporation"
    }

def cert_tool(domain: str) -> dict:
    """
    Fetch SSL/TLS certificate information for a given domain.

    Args:
        domain (str): Domain name to lookup

    Returns:
        dict: Certificate details
    """
    return {
        "issuer": "Let's Encrypt Authority X3",
        "valid_from": "2023-06-01",
        "valid_to": "2024-06-01",
        "key_type": "RSA 2048-bit",
        "san_names": ["example.com", "www.example.com"]
    }

# define whois agent
whois_agent = LlmAgent(
    name = "whois_agent",
    model="gemini-2.0-flash",
    instruction= """You are an agent that can fetch WHOIS record
    for a given domain and parse and come up a report. You may
    use whois_tool to fetch whois records. 
    """,
    tools=[whois_tool],
    output_key= "whois_record",
)

# cert agent 
cert_agent = LlmAgent(
    name = "cert_agent",
    model="gemini-2.0-flash",
    instruction= """You are an agent that can fetch SSL/TLS certificate
    information for a given domain and analyze its validity and security attributes,
    and come up with a succint report. You may use cert_tool to fetch 
    the SSL record.
    """,
    tools = [cert_tool],
    output_key = "cert_record",
)

# define a parallel agent that uses whois and cert agents
parallel_agent = ParallelAgent(
    name = "pipeline_agent",
    description= "Run multiple parallel agents in parallel to gather information about a domain.",
    sub_agents=[whois_agent, cert_agent], 
)

# aggregate the results
report_agent = LlmAgent(
    name = "report_agent",
    model="gemini-2.0-flash",
    instruction=""" You are an agent which would help in combining 
    gather information from multiple agents. You may use the google_search
    tool to validate and enrich the domain intelligence report.

    **Input Summaries :**
    - WHOIS Record: {whois_record}
    - Cert Record: {cert_record}

    **Output Format:**

    ## Domain Intelligence Report
    - A brief description of the domain
    ### WHOIS record summary
    - List key fields
    ### Certificate record summary
    - List key fields
    """,
    tools = [google_search]
)

# define sequential agent that uses parallel agent and report agent
root_agent = SequentialAgent(
    name = "domain_intel_agent",
    # Run parallel research first, then merge the results
    description = "Run parallel research agents and merge the results into a structured format.",
    sub_agents = [parallel_agent, report_agent]
)
