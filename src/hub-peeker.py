import argparse

from utils import github_api

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
    print(f"username: {username} and repository: {repo}")

    assets = github_api.fetch_assets(username, repo)

    for asset in assets:
        print(f"{asset.get('number')}. {asset.get('name')} --> {asset.get('download_url')} \n>>Downlaod Size:{asset.get('asset_size')} - content-type: {asset.get('asset_type')}")

else:
    print("Please provide with the <username> and <repo>!\nRun `hub-peeker -h` for usage information.")
