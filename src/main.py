from utils import json
from utils import github_api
from utils import system_info

print("#"*25)
print("HubPeeker ~ Version 1.0")
print("#"*25)
print(" ")

username = input("GitHub Username: ")
repo = input("GitHub Repository Name: ")

github_api.list_releases(username, repo)

system_info = json.loads(system_info.get_system_info())
print(system_info)
