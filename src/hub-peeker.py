import argparse
import os
import time
from pathlib import Path
from argparse import RawTextHelpFormatter

from utils import __version__, github_api, requests, size_of_fmt


def list_releases(username: str, repo: str):
    """Print assets from the list returned by `github_api.fetch_assets()` function.
    Prompt user to select an asset and print download URL of selected asset.
    Save important information (such as, release version) to a `.json` file.

    Args:
        - `username` (str): GitHub Username
        - `repo` (str): GitHub Repository name
    """

    assets = github_api.fetch_assets(username, repo)

    try:
        asset_len = len(assets)

        for asset in assets:
            recommend = ""
            if asset.get('recommend'):
                recommend = "[RECOMMENDED]"
            print(f"{asset.get('asset_number')}. {asset.get('asset_name')} {recommend}")

        while True:
            select_asset = int(input(f"\nPlease select a release to downloaded (1-{asset_len}): "))
            
            match select_asset:
                case 0:
                    print("You are not a computer, count from 1 ~! (ｏ ‵-′)ノ”(ノ﹏<。)")
                    continue

            if select_asset > asset_len:
                print(f"There are only {asset_len} assets and you selected {select_asset}, why (´･ω･`)?")
                continue
            asset_number = select_asset - 1

            download_url = assets[asset_number].get('asset_download_url')
            asset_filename = assets[asset_number].get('asset_name')
            user_os = assets[asset_number].get('user_os')
            # save_release_info(asset_number, assets)
            download_asset(download_url, asset_filename, user_os)
            return

    except Exception:
        response_code = assets.get('Response code')
        if response_code != 200 and response_code != None:
            match response_code:
                case 404:
                    print("Resource not found.")
            print("Looks like this repository does not have any releases or assets. (￣_￣|||)")
            return
        elif assets.get('Bad response'):
            response_msg = assets.get('Bad response')
        print(response_msg)
        return

# def save_release_info(asset_number: int, assets: list):
#     """Save user selected asset's release information to a `.json` file.

#     Args:
#         - `asset_number` (int): User selected asset's number (index).
#         - `assets` (list): List return by `github_api.fetch_release()` function.
#     """
#     if asset_number == None:
#         return
   
#     asset_data = {
#         f"{assets[asset_number].get('username')}": {
#             f"{assets[asset_number].get('repo')}": {
#                 "version": f"{assets[asset_number].get('release_version')}",
#                 "asset_name": f"{assets[asset_number].get('asset_name')}",
#                 "asset_type": f"{assets[asset_number].get('asset_type')}",
#                 "asset_download_url": f"{assets[asset_number].get('asset_download_url')}",
#                 "os": f"{assets[asset_number].get('user_os')}",
#                 "arch": f"{assets[asset_number].get('user_arch')}"
#             }
#         }
#     }

#     asset_data_json = json.dumps(asset_data, indent=4)

#     with open(f'{assets_data}', 'w') as outfile:
#         outfile.write(asset_data_json)


def download_asset(asset_download_url: str, filename: str, user_os: str):

    # Check whether user in on "Windows" OR "Linux"
    # and download to user's "Download" directory.
    if user_os == 'windows':
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        progress_bar = '='
    elif user_os == 'linux':
        progress_bar = '#'
        download_dir = os.path.expanduser('~/Downloads')

    # Create a subdirectory inside user's "Download" directory.
    subdirectory = "HubPeeker"
    full_path = os.path.join(download_dir, subdirectory)
    os.makedirs(full_path, exist_ok=True)
    
    # This is the path where the asset will be saved / downloaded.
    # "~/Downloads/HubPeeker/<asset_name>" OR "/home/<username>/Downloads/HubPeeker/<asset_name>" for Linux.
    # "C:\Users\<username>\Downloads\HubPeeker\<asset_name>" for Windows.
    file_path = os.path.join(full_path, filename)
    
    response = requests.get(asset_download_url, stream=True)
    # Get the total file size
    file_size = int(response.headers.get('Content-Length', 0))

    # Start the timer to calculate ETA and stuff..
    start_time = time.time()

    # Download the file with progress bar
    progress = 0
    with open(file_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1024):
            fd.write(chunk)
            progress += len(chunk)
            # Calculate the elapsed time and the estimated time remaining
            elapsed_time = time.time() - start_time
            eta = (file_size - progress) / progress * elapsed_time
            # Print out the progress bar with ETA
            print("\rDownloaded: %s / Total: %s [\033[92m%-50s\033[0m] %d%% - ETA: %ds" % (
                size_of_fmt.format_file_size(progress),
                size_of_fmt.format_file_size(file_size),
                f'{progress_bar}'*int(progress*50/file_size),
                int(progress*100/file_size),
                eta
            ), end='')

        print()
        # Calculate the total time taken for the download
        total_time = time.time() - start_time
        print("Download finished in %ds" % total_time)


# def check_updates():

#     if path.exists():
#         print("`assets.json` exists, checking for updates will be helpful.")
#         with open(f'{path}', 'r') as openfile:
#             assets = json.load(openfile)

#         print(assets.get(f'{username}').get(f'{repo}').get('version'))
#     else:
#         print("couldn't find `assets.json`, let's download something first to make history.")


#########################################################

parser = argparse.ArgumentParser(
    prog="hub-peeker", 
    description="Download Assets from GitHub Releases.", 
    epilog=f"""
Usage examples:
  - hub-peeker -u 'username' -r 'repo'
  - hub-peeker -i

Additional Information:
  Version: {__version__}
  License: MIT License
  Copyright (c) 2024 Cheap Nightbot
    """,
    formatter_class=RawTextHelpFormatter
)
parser.add_argument("-v", "--version", action='version', version=f'%(prog)s v{__version__}')
parser.add_argument("-u", "--username", help="GitHub Username the repository belongs to.")
parser.add_argument("-r", "--repo", help="GitHub repository name (to download assets from)")
parser.add_argument("-i", "--interactive", help="Enter interactive mode to input GitHub username and repository interactively.", action="store_true")
parser.add_argument("-U", "--update", help="Check for new version/release of already downloaded assets.", action="store_true")

parser._optionals.title = "Options"

args = parser.parse_args()

username = args.username
repo = args.repo

if args.interactive:
    username = input("GitHub Username: ")
    repo = input("GitHub Repository Name: ")

if username and repo != None:
    print(f"Checking release assets for `https://github.com/{username}/{repo}`")

    list_releases(username, repo)

else:
    print("Please provide with the <username> and <repo>!\nRun `hub-peeker -h` for usage information.")
