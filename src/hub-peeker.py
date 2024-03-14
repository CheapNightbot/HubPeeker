import argparse

from utils import github_api, json, system_info

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

print(f"username: {username} and repository: {repo}")

github_api.list_releases(username, repo)

system_info = json.loads(system_info.get_system_info())
print(system_info.get('platform'))
