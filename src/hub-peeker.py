import argparse
import os
import time
# from pathlib import Path

from utils import __version__, github_api, requests, size_of_fmt


def list_releases(username: str, repo: str):
    """Print assets from the list returned by `github_api.fetch_assets()` function.
    Prompt user to select an asset and print download URL of selected asset.

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
                recommend = "\033[92m[RECOMMENDED]\033[0m"
            print(f"{asset.get('asset_number')}. {asset.get('asset_name')} - ({size_of_fmt.format_file_size(asset.get('asset_size'))}) {recommend}")

        while True:
            try:
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
                download_asset(download_url, asset_filename, user_os)
                return
            except KeyboardInterrupt:
                print("\n")
                exit(1)

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


def download_asset(asset_download_url: str, filename: str, user_os: str):
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

    try:
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
        
        return "success"
    except KeyboardInterrupt:
        print("\nDownload has been cancelled!\nNOTE: This application does not support the resumption of downloads. If you initiate a download again (even for the same asset), it will start from the beginning and overwrite any previously downloaded content.")
        return "failed"


#########################################################

parser = argparse.ArgumentParser(
    prog="hub-peeker",
    usage="%(prog)s [options...]",
    description="Download Assets from GitHub Releases.",
    allow_abbrev=False,
    epilog=f"""
Usage examples:
  - hub-peeker -u 'username' -r 'repo'
  - hub-peeker -i

Additional Information:
  Version: {__version__}
  License: MIT License
  Copyright (c) 2024 Cheap Nightbot
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument("-v", "--version", action='version', version=f'%(prog)s v{__version__}')
parser.add_argument("-u", "--username", metavar="<USERNAME>", help="GitHub Username the repository belongs to.")
parser.add_argument("-r", "--repo", metavar="<REPO>", help="GitHub repository name (to download assets from)")
parser.add_argument("-i", "--interactive", help="Enter interactive mode to input GitHub username and repository interactively.", action="store_true")
parser.add_argument("-U", "--update", help="Check for new version/release of already downloaded assets.", action="store_true", default=True)
parser._optionals.title = "Options"

args = parser.parse_args()

#########################################################

def main():
    username = args.username
    repo = args.repo

    if args.interactive:
        username = input("GitHub Username: ")
        repo = input("GitHub Repository Name: ")

    if username and repo != None:
        print(f"Checking release assets for `https://github.com/{username}/{repo}`")

        list_releases(username, repo)

    else:
        parser.exit(status=1, message="Please provide with the <USERNAME> and <REPO>!\nRun `hub-peeker -h` for usage information.\n")


if __name__ == '__main__':
    main()
