from . import json, requests, system_info

# Create variables for `headers` and "Bad response"
# 'cause these were being repeated several times through out
# this file and "SonarLint" was annoying me with warning. ￣へ￣
headers = {'accept': 'application/vnd.github+json'}
response_key = "Bad response"

def validate_username_repo(username:str, repo:str):
    """Check if the given Username (user) and Repository exist on GitHub

    Args:
        - `username` (str): GitHub Username
        - `repo` (str): GitHub Repository name

    Returns:
        - `dict`: Return appropriate (pre-defined) message based on recieved response code as dictionary.
        - `200`: If given `username` and `repository` exists on GitHub, return `200`.
    """
    url = f"https://api.github.com/users/{username}"

    try:
        response = requests.get(url, headers)
    except ConnectionError:
        return  {f'{response_key}': "Connection Error! Make sure you are connected to the internet and try again. X﹏X"}
    
    if response.status_code != requests.codes.ok:
        match response.status_code:
            case 403:
                return {f'{response_key}': "API rate limit exceeded for your IP. Maybe, try again after sometime.\nSorry for this! Currently this CLI Application only relies on direct HTTP requests to GitHub API endpoints, thus GitHub rate limits it."}
        return {f'{response_key}': f"Couldn't find this user with username `{username}` on GitHub.\nMake sure you have entered the correct spelling."}
    else:
        url = f"https://api.github.com/repos/{username}/{repo}"
        response = requests.get(url, headers)

        if response.status_code != requests.codes.ok:
            return {f'{response_key}': f"Couldn't find this Repository `{repo}` under this `{username}` username.\nMake sure you have entered the correct spelling.\nAlso, please note that this CLI Application (currently) doesn't support downloading assets from Private Repositories. Thank you for your understanding!"}
        else:
            return requests.codes.ok


def fetch_assets(username: str, repo: str) -> list | dict:
    """Fetch the list of assets of latest release for a given GitHub repository.

    Args:
        - `username` (str): GitHub Username
        - `repo` (str): GitHub Repository name

    Returns:
       - `list`: Return dictionary of assets inside a list. 
       - `dict`: If something goes wrong, return error message as dictionary.
    """

    check_user_repo = validate_username_repo(username, repo)
    if check_user_repo != 200:
        return check_user_repo

    url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"
    
    try:
        response = requests.get(url, headers)
    except ConnectionError:
        return  {f'{response_key}': "Connection Error! Make sure you are connected to the internet and try again. X﹏X"}
    
    if response.status_code != requests.codes.ok:
        match response.status_code:
            case 403:
                return {f'{response_key}': "API rate limit exceeded for your IP. Maybe, try again after sometime.\nSorry for this! Currently this CLI Application only relies on direct HTTP requests to GitHub API endpoints, thus GitHub rate limits it."}
        response_code = {'Response code': response.status_code}
        return response_code

    response_json = json.loads(response.content)

    print(f"The latest release version / tag: {response_json.get('tag_name')}")
    print(f"There are {len(response_json.get('assets'))} assets available in the latest release.\n")
    
    user_system_info = json.loads(system_info.get_system_info())
    user_os = user_system_info.get("platform")
    user_arch = user_system_info.get("architecture")

    assets = []
    asset_number = 1

    for x in response_json.get("assets"):
        asset = {}
        asset['username'] = username
        asset['repo'] = repo
        asset['release_version'] = response_json.get('tag_name')
        asset['asset_number'] = asset_number
        asset['asset_name'] = x.get("name")
        asset['asset_download_url'] = x.get("browser_download_url")
        asset['asset_size'] = x.get("size")
        asset['asset_type'] = x.get("content_type")
        asset['user_os'] = user_os
        
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
                    asset['user_arch'] = arch
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
