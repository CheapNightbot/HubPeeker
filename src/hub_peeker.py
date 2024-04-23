import argparse
from pathlib import Path
from utils import __version__, github_api, json


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
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
)
parser.add_argument(
    "-u",
    "--username",
    metavar="<USERNAME>",
    help="GitHub Username the repository belongs to.",
)
parser.add_argument(
    "-r",
    "--repo",
    metavar="<REPO>",
    help="GitHub repository name (to download assets from)",
)
parser.add_argument(
    "-i",
    "--interactive",
    help="Enter interactive mode to input GitHub username and repository interactively.",
    action="store_true",
)
parser.add_argument(
    "-d",
    "--dir",
    metavar="<DIRECTORY_PATH>",
    help="Specify the download directory. Default to user's 'Download' directory.",
)
parser.add_argument(
    "-U",
    "--update",
    help="Check for new version/release of already downloaded assets. [WIP]",
    action="store_true",
    default=True,
)
parser._optionals.title = "Options"

args = parser.parse_args()


def parse_config():
    path = Path("./config.json")

    try:
        contents = path.read_text()
    except FileNotFoundError:
        return None
    else:
        config = json.loads(contents)
        download_path = config["download_path"]
        return download_path


def is_valid_sting(string):
    return bool(string and (string.isalnum() or not string.isspace()))


def main():

    username = args.username
    repo = args.repo
    download_path = args.dir

    try:

        if args.interactive:
            username = input("GitHub Username: ")
            while not is_valid_sting(username):
                username = input("GitHub Username: ")
            repo = input("GitHub Repository Name: ")
            while not is_valid_sting(repo):
                repo = input("GitHub Repository Name: ")

            download_dir = (
                parse_config()
                if parse_config()
                else Path("~/Downloads/HubPeeker/").expanduser()
            )
            download_path = input(
                f"Download Directory PATH (Default to `{download_dir}`): "
            )
            download_path = Path(download_path).expanduser()
            if download_path:
                save_path = input(
                    "Would you like save this path as default path for future downloads? [Y/N]: "
                )
                if save_path.lower() == "y":
                    path = Path("./config.json")
                    config = {"download_path": f"{download_path}"}
                    contents = json.dumps(config)
                    path.write_text(contents)

            else:
                download_path = download_dir

        if is_valid_sting(username) and is_valid_sting(repo):
            print(
                f"Checking release assets for `https://github.com/{username}/{repo}`\n"
            )

            download_dir = (
                parse_config()
                if parse_config()
                else Path("~/Downloads/HubPeeker/").expanduser()
            )
            download_path = (
                Path(download_path).expanduser() if download_path else download_dir
            )
            if args.dir:
                save_path = input(
                    "Would you like save this path as default path for future downloads? [Y/N]: "
                )
                if save_path.lower() == "y":
                    path = Path("./config.json")
                    config = {"download_path": f"{download_path}"}
                    contents = json.dumps(config)
                    path.write_text(contents)

            # 1
            check_user_repo = github_api.validate_username_repo(username, repo)
            if check_user_repo != 200:
                print(check_user_repo.get("Bad response"))
                return

            # 2
            assets = github_api.fetch_assets(username, repo)
            try:
                asset_len = len(assets)

                if asset_len <= 1:
                    if assets.get("Response code") or assets.get("Bad response"):
                        raise Exception

                # 3
                asset_number = github_api.list_assets(assets)
                download_url = assets[asset_number].get("asset_download_url")
                asset_filename = assets[asset_number].get("asset_name")
                user_os = assets[asset_number].get("user_os")

                # 4
                github_api.download_asset(
                    download_url, asset_filename, user_os, download_path
                )

            except Exception:
                response_code = assets.get("Response code")
                if response_code != 200 and response_code != None:
                    match response_code:
                        case 404:
                            print("Resource not found.")
                    print(
                        "Looks like this repository does not have any releases or assets. (￣_￣|||)"
                    )
                    return
                elif assets.get("Bad response"):
                    response_msg = assets.get("Bad response")
                print(response_msg)
                return

        else:
            parser.exit(
                status=1,
                message="Please provide with the <USERNAME> and <REPO>!\nRun `hub-peeker -h` for usage information.\n",
            )

    except KeyboardInterrupt:
        # `CTRL + C` is your friend ;)
        exit(code=1)


if __name__ == "__main__":
    main()
