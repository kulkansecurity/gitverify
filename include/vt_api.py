import os, requests

# VT API URL
VT_API_URL = "https://www.virustotal.com/api/v3/"
# Get an optional key to interact with the VT API
VT_API_KEY = os.environ.get("VT_API_KEY", None)

def vt_request_json(url):
    if VT_API_KEY:
        headers = {"x-apikey": f"{VT_API_KEY}"}
    else:
        headers = {}

    # Make a request to the VT API 
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to make request to the VirusTotal API: {url}. Status code: {response.status_code}")

def domain_report(domain):
    return vt_request_json(f"{VT_API_URL}/domains/{domain}")
