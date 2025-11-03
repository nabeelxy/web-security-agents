import requests
import os
from dotenv import load_dotenv
import time
from io import BytesIO
from PIL import Image

load_dotenv()

URLSCAN_API_KEY = os.environ.get('URLSCAN_API_KEY')

URLSCAN_SCAN_URL = 'https://urlscan.io/api/v1/scan'
URLSCAN_RESULT_URL = 'https://urlscan.io/api/v1/result/{}'
URLSCAN_SCREENSHOT_URL = 'https://urlscan.io/screenshots/{}.png'
URLSCAN_DOM_URL = 'https://urlscan.io/dom/{}'

def urlscan_scan(url):
    """
    Given a URL or Domain, submit it to scan in UrlScan service

    Args:
        url (str): URL or domain to scan
    Returns:
        dict: Scan results containing status, scan_id, and other metadata
    """
    headers = {'apikey': URLSCAN_API_KEY, "Content-Type": "application/json"}
    payload = {'url': url, 'visibility': 'public'}
    output = {}
    try:
        req = requests.post(URLSCAN_SCAN_URL, headers=headers, json=payload, verify=False)
        if req.status_code == 200:
            output = req.json()
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url':url}
    except requests.ConnectTimeout as e:
        output = {'ERROR': '##timed out', 'url':url}
    except Exception as e:
        print(e)
        output = {'ERROR': 'Unknown error', 'url':url}
    return output

def urlscan_get_result(scan_id, rtype='result'):
    headers = {'apikey': URLSCAN_API_KEY}
    output = {}
    url = URLSCAN_RESULT_URL.format(scan_id)
    if rtype == 'screenshot':
        url = URLSCAN_SCREENSHOT_URL.format(scan_id)
    elif rtype == 'dom':
        url = URLSCAN_DOM_URL.format(scan_id)

    retry = 0
    while retry < 3:
        try:
            req = requests.get(url, headers=headers, verify=False)
            if req.status_code == 200:
                #print(req)
                if rtype == 'result':
                    output = req.json()
                elif rtype == 'screenshot':
                    filename = "screenshots/{}.png".format(scan_id)
                    i = Image.open(BytesIO(req.content))
                    i.save(filename, "PNG")
                    output = {"screenshot": filename}
                elif rtype == 'dom':
                    filename = "dom/{}.html".format(scan_id)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(req.text)
                    output = {"dom": filename}
            elif req.status_code == 204:
                output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'scan_id': scan_id}
            if req.status_code != 404:
                break
        except requests.ConnectTimeout as e:
            output = {'ERROR': 'Timed out', 'scan_id':scan_id}
        except Exception as e:
            print(e)
            output = {'ERROR': 'Unknown error', 'scan_id':scan_id}
            break
        retry += 1
        time.sleep(5)  # Wait 2 seconds before retrying
    return output

def urlscan_query(url):
    scan = urlscan_scan(url)
    time.sleep(15)  # Add a delay to allow scanning to complete
    if scan != None and "ERROR" not in scan:
        scan_id = scan.get('uuid')
        report = urlscan_get_result(scan_id) if scan_id else {}
        return {
            'scan': scan,
            'report': report
        }
    else:
        return {
            'scan': scan,
            'report': {}
        }
    
def urlscan_query_scan_id(uuid):
    if uuid != None :
        report = urlscan_get_result(uuid)
        return {
            'scan': {'uuid': uuid},
            'report': report
        }
    else:
        return {
            'scan': {'uuid': uuid},
            'report': {}
        }


if __name__ == "__main__":
    #print(urlscan_query("paypal-verify.com"))
    #print(urlscan_query_scan_id("019a4616-2094-740e-8287-08f645e1278d"))
    print(urlscan_get_result("019a4616-2094-740e-8287-08f645e1278d", 'dom'))