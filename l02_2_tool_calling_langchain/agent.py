from langchain.agents import create_agent
import whois

def get_domain_whois(domain: str):
    """
    Given a domain name, get the WHOIS record.

    Args:
        domain (str): domain name
    Returns: 
        WHOIS_record: A JSON object containing WHOIS record details or None if lookup fails
    """
    try:
        result = whois.whois(domain)
        return result
    except whois.exceptions.WhoisDomainNotFoundError as e:
        return {"warning": "Domain not found"}
    except Exception as e:
        return {"error": "Unable to get WHOIS record"}

agent = create_agent(
    model="gemini-2.0-flash",
    tools=[get_domain_whois],
    system_prompt="""
        You are an expert web security analysis agent.
        You may use the get_domain_whois tool
        to learn the WHOIS record for the domain which takes
        a domain name such as google.com or meta.com as an input. 
        If the registrar of the domain is MarkMonitor or SPC, 
        the domain is likely to be a 
        brand protected. Further, domain organization or registrant
        is a reputed organization, the domain is likely to be benign.
        """,
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
