from knowledgebase import KnowledgeBase
from mcp.server.fastmcp import FastMCP
import json
import os

def get_reputation_signals(domain: str) -> dict:
    """
    Given the domain name, get reputation information related to the domain. It
    includes 
    - Tranco rank - rank identifying how popular a domain is. Lower the numerical value,
    more popular it is and more likely to be benign.
    - Crunchbase data - Crunchbase profiles 3 million companies in the world and presence
    in the crunchbase is a likely benign signal.

    Args:
        domain: domain name
    Returns:
        reputation signals - a dict containing tranco and crunchbase information
    """

    KnowledgeBase.init(os.path.join(os.path.dirname(__file__), "config.yml"))  

    output = {
        "is_in_tranco": False,
        "tranco_rank": "Unknown",
        "is_in_crunchbase": False,
        "is_public_domain": False
    }

    if domain in KnowledgeBase.tranco:
        output["is_in_tranco"] = True
        output["tranco_rank"] = KnowledgeBase.tranco[domain]
    if domain in KnowledgeBase.crunchbase:
        output["is_in_crunchbase"] = True
    if domain in KnowledgeBase.public_doms:
        output["is_public_domain"] = True

    return output
    
# create server
mcp_dominfo = FastMCP("Domain Reputation Server")

@mcp_dominfo.tool()
def get_domain_reputation_info(domain: str) -> str:
    """
    Given a domain name, collect reputation signals and return the result as a JSON string.
    Args:
        domain (str): Domain name to query

    Returns:
        JSON string containing reputation signals for the domain
    """
    return json.dump(get_reputation_signals(domain))

if __name__ == "__main__":
    KnowledgeBase.init(os.path.join(os.path.dirname(__file__), "config.yml"))
    mcp_dominfo.run(transport="stdio")