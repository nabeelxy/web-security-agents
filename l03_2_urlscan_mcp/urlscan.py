import requests
import os
from dotenv import load_dotenv
import time
from io import BytesIO
from PIL import Image
import pandas as pd

load_dotenv()

URLSCAN_API_KEY = os.environ.get('URLSCAN_API_KEY')

URLSCAN_SCAN_URL = 'https://urlscan.io/api/v1/scan'
URLSCAN_RESULT_URL = 'https://urlscan.io/api/v1/result/{}'
URLSCAN_SCREENSHOT_URL = 'https://urlscan.io/screenshots/{}.png'
URLSCAN_DOM_URL = 'https://urlscan.io/dom/{}'

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), '../data/screenshots')
DOM_DIR = os.path.join(os.path.dirname(__file__), '../data/dom')
URLSCAN_CACHE_FILE = os.path.join(os.path.dirname(__file__), '../data/urlscan_cache.csv')

# In a production system, use a more robust caching mechanism like Redis
class UrlKnowledge:
    cache = {}
    loaded = False

    @staticmethod
    def init():
        df = pd.read_csv(URLSCAN_CACHE_FILE)
        UrlKnowledge.cache = dict(zip(df['url'], df['uuid']))
        UrlKnowledge.loaded = True

    @staticmethod
    def update_cache(url, uuid):
        """
        Update the cache with new URL scan data and save to CSV

        Args:
        url (str): URL that was scanned
        uuid: Scan id

        """
        if not UrlKnowledge.loaded:
            UrlKnowledge.init()

        # Update cache dictionary
        url = url.strip("/")
        UrlKnowledge.cache[url] = uuid

        with open(URLSCAN_CACHE_FILE, 'a') as f:
            f.write(f"{url},{uuid}\n")

    @staticmethod
    def check_cache(url):
        """
        Check if URL has been previously scanned and retrieve its UUID

        Args:
            url (str): URL to check in cache
        Returns:
            str or None: UUID of cached scan if exists, otherwise None
        """
        if not UrlKnowledge.loaded:
            UrlKnowledge.init()
        if url in UrlKnowledge.cache:
            return UrlKnowledge.cache[url]
        if url.starts_with('http://'):
            url = url.replace('http://', '')
            if url in UrlKnowledge.cache:
                return UrlKnowledge.cache[url]
        elif url.startswith('https://'):
            url = url.replace('https://', '')
            if url in UrlKnowledge.cache:
                return UrlKnowledge.cache[url]
        else:
            url = "https://" + url
            if url in UrlKnowledge.cache:
                return UrlKnowledge.cache[url]
            url = "http://" + url
            if url in UrlKnowledge.cache:
                return UrlKnowledge.cache[url]
        return None


def urlscan_scan(url):
    """
    Given a URL or Domain, submit it to scan in UrlScan service

    Args:
        url (str): URL or domain to scan
    Returns:
        dict: Scan results containing status, scan_id, and other metadata
    """
    # Lookup Cache:
    uuid = UrlKnowledge.check_cache(url)
    if uuid:
        result = {
            "uuid": uuid,
            "status": "CACHED",
            "url": url
        }
        return result

    # Submit
    headers = {'api-key': URLSCAN_API_KEY, "Content-Type": "application/json"}
    payload = {'url': url, 'visibility': 'public'}
    output = {}
    try:
        req = requests.post(URLSCAN_SCAN_URL, headers=headers, json=payload, verify=False)
        if req.status_code == 200:
            output = req.json()
            if "uuid" in output:
                UrlKnowledge.update_cache(url, output["uuid"])
        elif req.status_code == 204:
            output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'url':url}
        else:
            output = {'ERROR': f'HTTP {req.status_code}', 'url': url}
    except requests.ConnectTimeout as e:
        print(e)
        output = {'ERROR': '##timed out', 'url':url}
    except Exception as e:
        print(e)
        output = {'ERROR': 'Unknown error', 'url':url}
    return output

def urlscan_get_result(scan_id, rtype='result'):
    headers = {'apikey': URLSCAN_API_KEY}
    output = {}
    cached = False
    url = URLSCAN_RESULT_URL.format(scan_id)
    if rtype == 'screenshot':
        url = URLSCAN_SCREENSHOT_URL.format(scan_id)
        filename = os.path.join(SCREENSHOTS_DIR, "{}.png".format(scan_id))
        if os.path.exists(filename):
            cached = True
            output = {"screenshot": filename, "cached": True}
        else:
            print(f"{filename} not found")
    elif rtype == 'dom':
        url = URLSCAN_DOM_URL.format(scan_id)
        filename = os.path.join(DOM_DIR, "{}.html".format(scan_id))
        if os.path.exists(filename):
            cached = True
            output = {"dom": filename, "cached": True}
        else:
            print(f"{filename} not found")

    retry = 0
    while not cached and retry < 3:
        try:
            req = requests.get(url, headers=headers, verify=False)
            if req.status_code == 200:
                #print(req)
                if rtype == 'result':
                    output = req.json()
                elif rtype == 'screenshot':
                    i = Image.open(BytesIO(req.content))
                    i.save(filename, "PNG")
                    output = {"screenshot": filename, "cached": False}
                elif rtype == 'dom':
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(req.text)
                    output = {"dom": filename, "cached": False}
            elif req.status_code == 204:
                output = {'ERROR': 'Received HTTP 204: You may have exceeded the rate limit', 'scan_id': scan_id}
            else:
                output = {'ERROR': f'HTTP {req.status_code}', 'scan_id': scan_id}
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

def urlscan_query(url, rtype='result'):
    scan = urlscan_scan(url)
    print(scan)
    time.sleep(15)  # Add a delay to allow scanning to complete
    if scan != None and "ERROR" not in scan:
        scan_id = scan.get('uuid')
        report = urlscan_get_result(scan_id, rtype) if scan_id else {}
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
    print(urlscan_query("inslagarm.com", "screenshot"))
    #print(urlscan_query_scan_id("019a4616-2094-740e-8287-08f645e1278d"))
    #print(urlscan_get_result("019a4616-2094-740e-8287-08f645e1278d", 'dom'))