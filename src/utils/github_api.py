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
    print(f"There are {len(response_json.get('assets'))} assets available in the latest release.\n")
    
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
        
        """
        If `user_os` (returned by `system_info.get_system_info()` function) string literal (e.g.: 'windows', 'linux')
        is in the release name string literal, then check if it (release name) also mentions one of the 
        CPU achitectures (returned by `system_info.get_system_info() as a list) and if it does (e.g.: 'app-release-v1.0-x86_64-windows.zip'),
        then add 'recommend' key with value `True` into `asset` dictionary. 
        """
        recommend = False
        if user_os in x.get("name").lower():
            for arch in user_arch:
                if arch in x.get("name").lower():
                    recommend = True
                    # maybe there are 3 architecture in `user_arch` (i.e.: 'amd64', 'x64', etc.).
                    # so, if it matches with the first or maybe second one, don't check for further
                    # and break out of this `for` loop. otherwise, if it only matches with first one
                    # in the list, it will set `recommend` to `True` (in the first iteration) and
                    # then for the rest it will just set it to `False` and will be return with
                    # `recommend = False` even if it was supposed to be `True`. 
                    # Sorry, for bad Inglish. <( _ _ )>
                    break
        
        asset['recommend'] = recommend
        assets.append(asset)
        asset_number += 1

    return assets
