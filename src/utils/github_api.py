import requests

from . import json, system_info


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

    print(f"The latest release version / tag: {response_json.get('tag_name')}")
    print(f"There are {len(response_json.get('assets'))} assets available in the latest release.")
    
    user_system_info = json.loads(system_info.get_system_info())
    user_os = user_system_info.get("platform")
    user_arch = user_system_info.get("architecture")

    assets = []
    asset_number = 1

    for x in response_json.get("assets"):
        asset = {}
        asset['number'] = asset_number
        asset['name'] = x.get("name")
        asset['download_url'] = x.get("browser_download_url")
        asset['asset_size'] = x.get("size")
        asset['asset_type'] = x.get("content_type")
        
        recommend = False
        if user_os in x.get("name").lower():
            for arch in user_arch:
                if arch in x.get("name").lower():
                    recommend = True
                    break
        
        asset['recommend'] = recommend
        assets.append(asset)
        asset_number += 1

    return assets
