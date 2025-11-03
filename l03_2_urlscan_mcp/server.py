from mcp.server.fastmcp import FastMCP
import json
import urlscan

# create server
mcp_urlscan = FastMCP("UrlScan Server")

@mcp_urlscan.tool()
def urlscan_query(url: str) -> str:
    """
    Given a url/domain name, get the UrlScan report.

    Args:
        url (str): url or domain name
    Returns: 
        UrlScan_report: A JSON string containing UrlScan scanning details and scan report
    """
    return json.dumps(urlscan.urlscan_query(url))

    

if __name__ == "__main__":
    mcp_urlscan.run(transport="stdio")