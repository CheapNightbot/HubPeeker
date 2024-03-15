import argparse

from utils import github_api


def list_releases(assets: list):
    """Print assets from the list returned by `github_api.fetch_assets()` function.
    Prompt user to select an asset and print download URL of selected asset.

    Args:
        - `assets` (list): List of assets. Each asset is a dictionary.
    """
    asset_len = len(assets)

    for asset in assets:
        recommend = ""
        if asset.get('recommend'):
            recommend = "[RECOMMENDED]"
        print(f"{asset.get('number')}. {asset.get('name')} {recommend}")

    while True:
        select_asset = int(input(f"Please select a release to downloaded (1-{asset_len}): "))
        
        if select_asset > asset_len:
            print(f"There are only {asset_len} assets and you selected {select_asset}, why (´･ω･`)?")
            continue
        asset_number = select_asset - 1
        print(assets[asset_number].get('download_url'))
        break


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username")
parser.add_argument("-r", "--repo")
parser.add_argument("-U", "--update", action="store_true")
parser.add_argument("-i", "--interactive", action="store_true")

args = parser.parse_args()

username = args.username
repo = args.repo


if args.interactive:
    username = input("GitHub Username: ")
    repo = input("GitHub Repository Name: ")

if username and repo != None:
    print(f"Checking release assets for `https://github.com/{username}/{repo}`")

    assets = github_api.fetch_assets(username, repo)

    list_releases(assets)

else:
    print("Please provide with the <username> and <repo>!\nRun `hub-peeker -h` for usage information.")
