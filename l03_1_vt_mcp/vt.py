import requests
import os
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.environ.get('VT_API_KEY')

VT_SCAN_URL = 'https://www.virustotal.com/vtapi/v2/url/scan'
VT_REPORT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'

def vt_scan(url):
    """
    Given a URL or Domain, submit it to scan in VirusTotal

    Args:
        url (str): URL or domain to scan
    Returns:
        dict: Scan results containing status, scan_id, and other metadata
    """
    params = {'apikey': VT_API_KEY, 'url':url}
    output = {}
    try:
        req = requests.post(VT_SCAN_URL, data=params, verify=False)
        if req.status_code == 200:
            output = req.json()
            if output['response_code'] == -1:
                output['url'] = url
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url':url}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url':url}
    return output

def vt_get_report(resource):
    params = {'apikey': VT_API_KEY, 'resource':resource, 'allinfo': 'true'}
    output = {}
    try:
        req = requests.get(VT_REPORT_URL, params=params, verify=False)
        if req.status_code == 200:
            output = req.json()
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url': resource}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url':resource}
    return output

def vt_query(url):
    scan = vt_scan(url)
    if scan != None and "ERROR" not in scan:
        scan_id = scan.get('scan_id')
        report = vt_get_report(scan_id) if scan_id else {}
        return {
            'scan': scan,
            'report': report
        }
    else:
        return {
            'scan': scan,
            'report': {}
        }

#if __name__ == "__main__":
#    print(vt_query("paypal-verify.com"))