import argparse

from utils import github_api, json


def list_releases(assets: list):
    """Print assets from the list returned by `github_api.fetch_assets()` function.
    Prompt user to select an asset and print download URL of selected asset.
    Save import information (such as, release version) to a `.json` file.

    Args:
        - `assets` (list): List of assets. Each asset is a dictionary.
    """
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

            print(assets[asset_number].get('asset_download_url'))
            return asset_number

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

def save_release_info(asset_number: int):

    if asset_number == None:
        return

    asset_data = {
        f"{assets[asset_number].get('username')}": {

            f"{assets[asset_number].get('repo')}": {

                "version": f"{assets[asset_number].get('release_version')}",
                "asset_name": f"{assets[asset_number].get('asset_name')}",
                    "asset_type": f"{assets[asset_number].get('asset_type')}",
                    "asset_download_url": f"{assets[asset_number].get('asset_download_url')}",
                    "os": "windows"
                }
            }
        }

    asset_data_json = json.dumps(asset_data, indent=4)

    with open('assets.json', 'w') as outfile:
        outfile.write(asset_data_json)


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
    user_select_asset = list_releases(assets)
    save_release_info(user_select_asset)

else:
    print("Please provide with the <username> and <repo>!\nRun `hub-peeker -h` for usage information.")
