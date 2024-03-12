import requests
from . import json

# Fetch the list of assets of latest release for a given repository
def list_releases(username, repo):

    url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    response = requests.get(url)
    
    if response.status_code != requests.codes.ok:
        print("OH MA BOT, couldn't get data from GitHub.")
        return f'Response code: {response.status_code}'

    response_json = json.loads((response.content))

    release_tag = response_json.get("tag_name")
    assets = response_json.get("assets")

    print(f"The latest release version / tag: {release_tag}")
    print(f"There are {len(assets)} assets available in the latest release.")
    
    x = 1
    for asset in assets:
        print(f"{x}. {asset["name"]}")
        x += 1