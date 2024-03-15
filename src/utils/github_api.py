import requests

from . import json


def fetch_assets(username: str, repo: str) -> list:
    """Fetch the list of assets of latest release for a given GitHub repository.

    Args:
        - `username` (str): GitHub Username
        - `repo` (str): GitHub Repository name

    Returns:
       - `list`: Return dictionary of assets inside a list.
    """

    url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    response = requests.get(url)
    
    if response.status_code != requests.codes.ok:
        print("OH MA BOT, couldn't get data from GitHub.")
        return f'Response code: {response.status_code}'

    response_json = json.loads((response.content))

    print(f"The latest release version / tag: {response_json.get("tag_name")}")
    print(f"There are {len(response_json.get("assets"))} assets available in the latest release.")

    assets = []
    asset_number = 1

    for x in response_json.get("assets"):
        asset = {}
        asset['number'] = asset_number
        asset['name'] = x.get("name")
        asset['asset_type'] = x.get("content_type")
        asset['asset_size'] = x.get("size")
        asset['download_url'] = x.get("browser_download_url")
        assets.append(asset)
        asset_number += 1

    return assets
