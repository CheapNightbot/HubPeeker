import argparse

from utils import __version__, github_api

# from pathlib import Path


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
parser.add_argument("-U", "--update", help="Check for new version/release of already downloaded assets. [WIP]", action="store_true", default=True)
parser._optionals.title = "Options"

args = parser.parse_args()


def main():

    username = args.username
    repo = args.repo

    if args.interactive:
        username = input("GitHub Username: ")
        repo = input("GitHub Repository Name: ")

    if username and repo != None:
        print(f"Checking release assets for `https://github.com/{username}/{repo}`")

        github_api.list_assets(username, repo)

    else:
        parser.exit(status=1, message="Please provide with the <USERNAME> and <REPO>!\nRun `hub-peeker -h` for usage information.\n")


if __name__ == '__main__':
    main()
