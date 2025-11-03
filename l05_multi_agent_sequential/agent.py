from google.adk.agents import LlmAgent, SequentialAgent

def nslookup_tool(domain: str) -> str:
    """
    Perform nslookup to retrieve IP address for a given domain. In 
    other words, it returns the IP address on which a domain is hosted.

    Args:
        domain (str): Domain name to lookup

    Returns:
        str: IP address of the domain
    """
    return "1.1.1.1"

def asn_tool(ip: str) -> dict:
    """
    Perform ASN lookup for a given IP address.

    Args:
        ip (str): IP address to lookup

    Returns:
        dict: ASN details including ASN number, organization, and geolocation
    """
    return {"asn": "AS13335", 
            "org": "Cloudflare, Inc.", 
            "country": "United States"}

# define nslookup agent
nslookup_agent = LlmAgent(
    name = "nslookup_agent",
    model = "gemini-2.5-flash",
    instruction = """
        You are an agent that provides IP adress of a domain using nslookup_tool.
        nslookup_tool tool finds the IP address for a given domain. If you are 
        asked to find the ASN information of a domain, you need to use this
        agent to first find IP information.
        """,
    output_key = "ip_address",
    tools = [nslookup_tool]
)

# define asn agent 
asn_agent = LlmAgent(
    name = "asn_agent",
    model = "gemini-2.5-flash",
    instruction = """
        You are an agent that provides the ASN and geolocation of a given {ip_address} using 
        the asn_tool. asn_tool tool finds the asn information for a given ip address.
        """,
    tools = [asn_tool]
)

# define sequential agent that uses nslookup and asn agents
root_agent = SequentialAgent(
    name = "pipeline_agent",
    sub_agents=[nslookup_agent, asn_agent], 
)