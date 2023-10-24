import os, requests, base64, re

# GitHub API URL
GITHUB_API_URL = "https://api.github.com/repos/"
# Get an optional token to get better rate limits
GITHUB_TOKEN = os.environ.get("GH_ACCESS_TOKEN", None)

def github_request_json(url):
    if GITHUB_TOKEN:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    else:
        headers = {}

    # Make a request to the GitHub API 
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to make request to the github API: {url}. Status code: {response.status_code} - Response: {response.json()}")


def fetch_domains_from_code(repository):
    matches = github_request_json(f"https://api.github.com/search/code?q=repo:{repository}%20in:file%20http")
    for m in matches['items']:
        code = base64.b64decode(github_request_json(m['url'])["content"]).decode()
        # This by no means is a complete regex - do not rely on this code picking up ALL possible domains
        url_pattern = r'https?://([\w.-]+)'
        # Find all matches in the code content
        matches = re.findall(url_pattern, code)
        return matches


def fetch_repository(github_url):
    # Extract owner and repository name from the GitHub URL
    parts = github_url.strip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    return github_request_json(f"{GITHUB_API_URL}{owner}/{repo_name}")

def fetch_contributors(repo_obj):
    return github_request_json(repo_obj.get('contributors_url'))

def fetch_issues_and_prs(repo_obj):
    return github_request_json(repo_obj.get('issues_url').replace("{/number}","?state=all"))

def fetch_contributor(contributor_obj):
    return github_request_json(contributor_obj['url'])

def fetch_contributor_contributions(repo_obj, contributor_obj):
    return github_request_json(repo_obj.get('commits_url').replace("{/sha}",f"?author={contributor_obj['login']}"))

def json_request(url):
    # Make a request to the GitHub API 
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch information from {url}. Status code: {response.status_code}")

