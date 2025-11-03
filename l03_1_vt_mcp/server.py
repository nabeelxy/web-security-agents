from mcp.server.fastmcp import FastMCP
import json
import vt

# create server
mcp_vt = FastMCP("VirusTotal Server")

@mcp_vt.tool()
def vt_query(url: str) -> str:
    """
    Given a url/domain name, get the VirusTotal report.

    Args:
        url (str): url or domain name
    Returns: 
        VT_report: A JSON string containing VirusTotal scanning details and scan report
    """
    return json.dumps(vt.vt_query(url))

    

if __name__ == "__main__":
    mcp_vt.run(transport="stdio")