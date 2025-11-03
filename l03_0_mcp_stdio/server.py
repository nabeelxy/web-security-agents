from mcp.server.fastmcp import FastMCP
import whois
import json
from whois_util import get_domain_whois_v2

# create server
mcp = FastMCP("WHOIS Server")

@mcp.tool()
def get_domain_whois_mcp(domain: str) -> str:
    """
    Given a domain name, get the WHOIS record.

    Args:
        domain (str): domain name
    Returns: 
        WHOIS_record: A JSON string containing WHOIS record details or None if lookup fails
    """
    return json.dumps(get_domain_whois_v2(domain))

    

if __name__ == "__main__":
    mcp.run(transport="stdio")