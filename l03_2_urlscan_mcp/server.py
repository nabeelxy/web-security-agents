from mcp.server.fastmcp import FastMCP
import json
import urlscan
from google import genai
from google.genai import types
import os

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), '../data/screenshots')

SCREENSHOT_ANALYSIS_PROMPT = """
You are an expert cyber security a.ssistant analyzing web screenshots for 
potential security risks and anomalies.
Your task is to analyze the visual elements, detect suspicious components, potential phishing indicators, 
malicious design patterns, and provide a comprehensive security assessment.

Please format your analysis output into the following JSON format:
{
"brands": "A list of brands detected from the screenshot",
"security_risks": "A list of identified potential security risks",
"lure": "Description of any potential social engineering or phishing lures",
"suspicious_elements": "Visual elements that might indicate a security threat",
"additional_observations": ""Other noteworthy security-related observations"
}
"""
def analyze_screenshot_file(screenshot_file):
    with open(screenshot_file, 'rb') as f:
        image_bytes = f.read()

    client = genai.Client()
    response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents=[
        types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
        ),
        SCREENSHOT_ANALYSIS_PROMPT
    ]
    )

    return response.text

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

@mcp_urlscan.tool()
def urlscan_screenshot_analysis(url: str) -> str:
    """
    Perform UrlScan and analyze screenshot for security risks.

    Args:
        url (str): URL or domain to scan and analyze
    Returns:
        Analysis result: A JSON string with screenshot security analysis
    """
    response = urlscan.urlscan_query(url, "screenshot")
    print(f"url = {url}")
    print(f"response = {response}")
    screenshot_path = response.get('report', {}).get('screenshot', '')
    if not screenshot_path or not os.path.exists(screenshot_path):
        return json.dumps({
            "Error": "unable to get the screenshot"})

    return analyze_screenshot_file(screenshot_path)

if __name__ == "__main__":
    mcp_urlscan.run(transport="stdio")