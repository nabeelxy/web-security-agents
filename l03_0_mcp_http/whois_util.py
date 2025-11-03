import whois
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHO_ENDPOINT = "http://api.whoapi.com/?domain={}&r=whois&apikey={}"

def get_domain_whois_v2(domain: str) -> dict:
    """
    Given a domain name, get the WHOIS record.

    Args:
        domain (str): domain name
    Returns: 
        WHOIS_record: A JSON string containing WHOIS record details or None if lookup fails
    """
    output = {}
    url = WHO_ENDPOINT.format(domain, os.environ.get("WHO_API_KEY"))
    try:
        req = requests.get(url, verify=False)
        if req.status_code == 200:
            output = req.json()
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url':url}
    except requests.ConnectTimeout as e:
        output = {'ERROR': 'Timed out', 'domain':domain}
    except Exception as e:
        print(e)
        output = {'ERROR': 'Unable to collect', 'domain':domain}
    return output

def get_domain_whois(domain: str) -> dict:
    """
    Given a domain name, get the WHOIS record.

    Args:
        domain (str): domain name
    Returns: 
        WHOIS_record: A JSON string containing WHOIS record details or None if lookup fails
    """
    try:
        result = whois.whois(domain)
        return json.dumps(result)
    except whois.exceptions.WhoisDomainNotFoundError as e:
        return json.dumps({"warning": "Domain not found"})
    except Exception as e:
        return json.dumps({"error": "Unable to get WHOIS record"})
    
if __name__ == "__main__":
    print(get_domain_whois_v2("paypal.com"))
