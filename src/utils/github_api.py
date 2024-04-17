import os
import time

from . import json, requests, system_info, pretty_bytes

# Create variables for `headers` and "Bad response"
# 'cause these were being repeated several times through out
# this file and "SonarLint" was annoying me with warning. ￣へ￣
headers = {"accept": "application/vnd.github+json"}
response_key = "Bad response"


# Step 1 ~ Check if the given Username & Repo exist on GitHub
def validate_username_repo(username: str, repo: str):
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
    except requests.exceptions.ConnectionError:
        return {
            f"{response_key}": "Connection Error! Make sure you are connected to the internet and try again. X﹏X"
        }

    if response.status_code != requests.codes.ok:
        match response.status_code:
            case 403:
                return {
                    f"{response_key}": "API rate limit exceeded for your IP. Maybe, try again after sometime.\nSorry for this! Currently this CLI Application only relies on direct HTTP requests to GitHub API endpoints, thus GitHub rate limits it."
                }
        return {
            f"{response_key}": f"Couldn't find this user with username `{username}` on GitHub.\nMake sure you have entered the correct spelling."
        }
    else:
        url = f"https://api.github.com/repos/{username}/{repo}"
        response = requests.get(url, headers)

        if response.status_code != requests.codes.ok:
            return {
                f"{response_key}": f"Couldn't find this Repository `{repo}` under this `{username}` username.\nMake sure you have entered the correct spelling.\nAlso, please note that this CLI Application (currently) doesn't support downloading assets from Private Repositories. Thank you for your understanding!"
            }
        else:
            return requests.codes.ok


# Step 2 ~ Fetch the assets from the latest release
def fetch_assets(username: str, repo: str) -> list | dict:
    """Fetch the list of assets of latest release for a given GitHub repository.

    Args:
        - `username` (str): GitHub Username
        - `repo` (str): GitHub Repository name

    Returns:
       - `list`: Return dictionary of assets inside a list.
       - `dict`: If something goes wrong, return error message as dictionary.
    """

    url = f"https://api.github.com/repos/{username}/{repo}/releases/latest"

    try:
        response = requests.get(url, headers)
    except requests.exceptions.ConnectionError:
        return {
            f"{response_key}": "Connection Error! Make sure you are connected to the internet and try again. X﹏X"
        }

    if response.status_code != requests.codes.ok:
        match response.status_code:
            case 403:
                return {
                    f"{response_key}": "API rate limit exceeded for your IP. Maybe, try again after sometime.\nSorry for this! Currently this CLI Application only relies on direct HTTP requests to GitHub API endpoints, thus GitHub rate limits it."
                }
        response_code = {"Response code": response.status_code}
        return response_code

    response_json = json.loads(response.content)

    print(f"The latest release version / tag: {response_json.get('tag_name')}")
    print(
        f"There are {len(response_json.get('assets'))} assets available in the latest release.\n"
    )

    user_system_info = json.loads(system_info.get_system_info())
    user_os = user_system_info.get("platform")
    user_arch = sorted(user_system_info.get("architecture"))

    assets = []
    asset_number = 1

    tag_name = response_json.get("tag_name").lower()
    for x in response_json.get("assets"):
        name = x.get("name").lower()
        arch = next((arch for arch in user_arch if arch in name), "None")

        asset = {
            "username": username,
            "repo": repo,
            "release_version": tag_name,
            "asset_number": asset_number,
            "asset_name": name,
            "asset_download_url": x.get("browser_download_url"),
            "asset_size": x.get("size"),
            "asset_type": x.get("content_type"),
            "user_os": user_os,
            "user_arch": arch,
            "recommend": True if user_os in name and arch in name else False,
        }
        assets.append(asset)
        asset_number += 1

    return assets


# Step 3 ~ List all the available assets
def list_assets(assets):
    """Print assets from the list returned by `fetch_assets()` function.
    Prompt user to select an asset and print download URL of selected asset.

    Args:
        - `username` (str): GitHub Username
        - `repo` (str): GitHub Repository name
    """

    asset_len = len(assets)

    header = (
        "\033[4;1m{num:<4}\033[0m \033[4;1m{name:50}\033[0m \033[4;1m{size:}\033[0m"
    )
    print(header.format(num="NO.", name="ASSET NAME", size="ASSET SIZE"))

    for asset in assets:
        num = asset.get("asset_number")
        name = asset.get("asset_name")
        size = pretty_bytes.pretty_bytes(asset.get("asset_size"))
        recommend = ""
        if asset.get("recommend"):
            recommend = "\033[92m[RECOMMENDED]\033[0m"
        print(f"{num:<4} {name.ljust(50, '.')} {size} {recommend}")

    while True:
        try:
            select_asset = int(
                input(f"\nPlease select an asset to download (1-{asset_len}): ")
            )

            match select_asset:
                case 0:
                    print(
                        "You are not a computer, count from 1 ~! (ｏ ‵-′)ノ”(ノ﹏<。)"
                    )
                    continue

            if select_asset > asset_len:
                print(
                    f"There are only {asset_len} assets and you selected {select_asset}, why (´･ω･`)?"
                )
                continue

            asset_number = select_asset - 1
            return asset_number
        except KeyboardInterrupt:
            print("\n")
            exit(1)


# Step 4 ~ Download the user selected asset
def download_asset(asset_download_url: str, filename: str, user_os: str, download_path=None):
    """Download Asset into user's `Download` directory, inside `HubPeeker` sub-directory.

    Args:
        - `asset_download_url` (str): Asset download URL.
        - `filename` (str): Asset will be saved with this name.
        - `user_os` (str): User's Operating System (i.e.: Windows or Linux).

    Returns:
        - `str`: Return string literal 'success' after successfully downloading asset or 'failed' if user interrupts it.
    """
    # Check whether user in on "Windows" OR "Linux"
    # and download to user's "Download" directory.
    if user_os == "windows":
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        progress_bar = "="
    elif user_os == "linux":
        progress_bar = "#"
        download_dir = os.path.expanduser("~/Downloads")

    # Create a subdirectory inside user's "Download" directory.
    subdirectory = "HubPeeker"
    download_path = download_path if download_path else os.path.join(download_dir, subdirectory)
    os.makedirs(download_path, exist_ok=True)

    # This is the path where the asset will be saved / downloaded.
    # "~/Downloads/HubPeeker/<asset_name>" OR "/home/<username>/Downloads/HubPeeker/<asset_name>" for Linux.
    # "C:\Users\<username>\Downloads\HubPeeker\<asset_name>" for Windows.
    file_path = os.path.join(download_path, filename)

    response = requests.get(asset_download_url, stream=True)
    # Get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # Start the timer to calculate ETA and stuff..
    start_time = time.time()

    try:
        # Download the file with progress bar
        progress = 0
        with open(file_path, "wb") as fd:
            for chunk in response.iter_content(chunk_size=1024):
                fd.write(chunk)
                progress += len(chunk)
                # Calculate the elapsed time and the estimated time remaining
                elapsed_time = time.time() - start_time
                eta = (file_size - progress) / progress * elapsed_time
                # Print out the progress bar with ETA
                print(
                    "\rDownloaded: %s / Total: %s [\033[92m%-50s\033[0m] %d%% - ETA: %ds"
                    % (
                        pretty_bytes.pretty_bytes(progress),
                        pretty_bytes.pretty_bytes(file_size),
                        f"{progress_bar}" * int(progress * 50 / file_size),
                        int(progress * 100 / file_size),
                        eta,
                    ),
                    end="",
                )

            print()
            # Calculate the total time taken for the download
            total_time = time.time() - start_time
            print("Download finished in %ds" % total_time)
        print(f"Downloaded asset can be found here: '{download_path}'")
        return "success"
    except KeyboardInterrupt:
        print(
            "\nDownload has been cancelled!\nNOTE: This application does not support the resumption of downloads. If you initiate a download again (even for the same asset), it will start from the beginning and overwrite any previously downloaded content."
        )
        return "failed"
