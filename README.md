> [!IMPORTANT]
> **Reason for Archive**: Even though it was great for learning, but in reality, it doesn't provide any value at all. So, I don't feel like wasting my only time working further on it.

<hr />

<div align="center">

[![HubPeeker Banner](docs/images/hub-peeker_banner.png)](#) 

[![Version](https://img.shields.io/badge/version-0.6.9_(alpha)-blue)](#)
[![Python](https://badgen.net/pypi/python/black)](#)

[![License](https://forthebadge.com/images/badges/license-mit.svg)](LICENSE) 
[![Spaghetti Code](https://forthebadge.com/images/badges/contains-tasty-spaghetti-code.svg)](#) 
[![Kinda SFW](https://forthebadge.com/images/badges/kinda-sfw.svg)](#) 

[![Python](https://forthebadge.com/images/badges/made-in-python.svg)](#)
[![Coffee](https://forthebadge.com/images/badges/powered-by-coffee.svg)](#) 
[![It's FREE](docs/images/it's-free.svg)](#)

</div>

***

**HubPeeker** is a simple command-line application written in **Python** to download release assets from **GitHub**. It uses simple HTTP requests to retrieve and download assets from GitHub API endpoint.

# Table of Content

* [FEATURES](#features)
  * [Planned / In Progress](#planned--in-progress)
  * [Testing](#testing)
* [INSTALLATION](#installation)
  * [Binaries](#binaries)
  * [Cloning and Running the Application](#cloning-and-running-the-application)
* [USAGE AND OPTIONS](#usage-and-options)
  * [Quick Overview](#quick-overview)
  * [Explanation of each Option](#explanation-of-each-option)
* [FAQ](#faq)
  * [Why I Created This?](#why-i-created-this)
  * [What's Up With The Name?](#whats-up-with-the-name)
  * [What's Up With That Logo?](#whats-up-with-that-logo)

# FEATURES

> ⚠ __WORK IN PROGRESS! LACKS SOME FEATURES__.
> This project is currently in the early stages of development.
> > - It does not currently have ability to resume download.
> > - There is no way to track the version of downloaded asset and check if there is new release availabe on GitHub. (Though, I had created `.json` file for it, but it was getting all over the place, so removed).

<h1 align="center">
  <img src="docs/images/HubPeeker - FlowChart.png" />
</h1>

<details>
  <summary>DEMO</summary>
  <p align="center">
    <img src="docs/images/HubPeeker - DEMO.gif" />
  </p>
</details>

- List all the available assets from the latest release of the given GitHub Repository.
- Detect and suggest an asset based on the user's operating system and CPU architecture.
- Show the asset size (in human-readable format using `base-2`).
- User can select an asset and it will download the selected asset inside "HubPeeker" sub-directory to the user's "Download" directory.
  - OR Users can specify the download directory.

## Planned / In Progress
- [ ] Use local database (most likely **SQLite**) to track the downloaded version of each asset and compare downloaded version with the latest version on GitHub. (Likely to automate the download if there is new release).
- [ ] Have ability to pause and resume the download of asset(s).
- [ ] The end goal of this project is to automate the download of the asset(s) from the GitHub Releases once the user has downloaded an asset and there is new version/release for that asset is available.
- [ ] Properly setup and maintain this repository !!

## Testing

As the project is still evolving, comprehensive tests have not been written yet. This is something I acknowledge and plan to address as the project becomes more stable.

# INSTALLATION

## Binaries

I plan to provide binaries for different operating systems in the future. However, as the project is still in the early stages, these are not available yet. I will update this section as soon as they are ready.

Thank you for your understanding!

## Cloning and Running the Application

Make sure you have **Python 3.8** or higher installed on your system.

- Clone the repository:
  - `git clone https://github.com/CheapNightbot/HubPeeker.git`
- [Create virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) and activate it. [Optional]
- Run `python -m pip install -r requirements.txt`.
- Change directory into `src` by `cd src`.
- Run `python hub_peeker.py -h`.

# USAGE AND OPTIONS

## Quick Overview

```
Usage: hub-peeker [options...]
```

```
Options:
  -h, --help                  show this help message and exit
  -v, --version               show program's version number and exit
  -u, --username <USERNAME>   GitHub Username the repository belongs to.
  -r, --repo <REPO>           GitHub repository name (to download assets from)
  -i, --interactive           Enter interactive mode to input GitHub username and repository interactively.
  -d, --dir <DIRECTORY>       Specify the download directory. Default to user's 'Download' directory.
  -U, --update                Check for new version/release of already downloaded assets.
```

## Explanation of each Option

* `-h` or `--help`: Prints the help information and some additional information about the application (and exits).

* `-v` or `--version`: Prints the current version of the application (and exits).

* `-u <USERNAME>` or `--username <USERNAME>`: Username flag/option followed by the GitHub Username of the repository owner you want to download asset from.
  
  * Example:
    
    * `hub-peeker -u 'cheapnightbot'`
    
    * `hub-peeker --username 'CheapNightbot'`
  
  * See, the username is NOT case-sensitive.
  
  * Using quotes (single or double) around username is not neccesary, but to be safe, it's good to use quotes around them.

* `-r <REPO>` or `--repo <REPO>`: Repository flag/option followed by the GitHub Repository name you want to download asset from.
  
  * Example:
    
    * `hub-peeker -r 'hubpeeker'`
    
    * `hub-peeker --repo 'HubPeeker'`
  
  * Same as the username flag. Use one of them, either sort one `-r` or long `--repo` one.

> **NOTE**: The username option/flag (i.e.: `-u/--username`) and repository option/flag (i.e.: `-r/--repo`), both must be provided together.
> - For example: `hub-peeker -u 'cheapnightbot' -r 'hubpeeker'`.
> 
> > Also, the order does NOT matter. You may use the `-r` flag before the `-u` flag and vice-versa.
> 
> Otherwise, use the `-i` (sort version) or `--interactive` (long version) option/flag:

* `-i` or `--interactive`: When provided, it will use **Python**'s `input()` function to prompt for the GitHub Username and Repository Name one by one.

  * When providing this option, there is no need to provide any other options. Though, currently, it will not stop you from doing so, but yeah..

  * Example: `hub-peeker -i` or `hub-peeker --interactive`

* `-d` or `--dir`: Directory flag/option followed by the directory path where the selected asset will be downloaded/saved.

  * Example:

    * `hub-peeker -d 'F:/GitHub/Assets'`
    * `hub-peeker -dir 'C:/SomeFolder'`

  * You may prefix `~` for your Home directory and `.` for the current directory (where the applicaion ran from):

    * `hub-peeker -d '~/Desktop'`: will save asset to your Desktop.

    * `hub-peeker -d './HubPeeker'`: will save asset to the current directory inside 'HubPeeker' sub-directory.

* `-U` or `--update`: Currently, this one is useless. The purpose of this will be to check if our database file exists and if there are any asset downloaded before and if yes, we will check for the new version / release and prompt to download appropriate asset.

# FAQ

## Why I Created This?

The other day, I was using Ubuntu and needed to install a CLI application. However, the version available on APT was a few releases behind the latest version on GitHub (not few, but basically outdated and most likely unmaintained). Luckly, they've provided a `.deb` asset in their GitHub releases.  So, I was like, “Why not grab the `.deb` from GitHub to get the latest version?”.

But, I wasn’t sure if installing the `.deb` from GitHub would give me updates like `apt update` does. So, it looked like I’d have to manually download the `.deb` every time a new release drops. Initially, I attempted to automate the download and installation of the `.deb` package from GitHub Releases using a Bash Script, but let’s just say it didn’t go as planned (but worked though).

Fast forward a bit, I had to switch to Windows (don’t ask, personal stuff), and me forgot about it. Then, while switching between Ubuntu (inside WSL) and Windows, I found this Static Site Generator (SSG) called Hugo. Now, Hugo had pre-built binaries for both Windows and Linux. So, *I had to download from (same) GitHub Releases for two different OS*.

So, I thought, "What if there was something that can figure out my OS, Architecture and suggest the right asset (as there were 20+ assets there) and download it for me next time there's new release?". And that’s how “HubPeeker” was born.

This time around, I set myself a challenge to avoid using third-party Python packages as much as possible. Instead, I aimed to stick with standard Python packages or code the basics myself. However, I did end up using the `requests` library. I’ve worked with it before, and honestly, coding something like that from scratch is way beyond my current skill level. As for `urllib`, let’s just say "no-no square".

## What's Up With The Name?

- **GitHub** → Git + Hub = Stores '*git*' repositories. 😃
- **HubPeeker** → Hub + Peeker = *Peeks* (checks) at '(Git)*Hub*', here for Latest Release and Assets. 😀

Um, email (check profile) can be used to ask for further explanation. (⊙_⊙;)

## What's Up With That Logo?

Okay, so the realization was late of the name "HubPeeker" being or sounding sus.. but at the end, I went with the joke and decided to use the same logo (PH), BUT reversed to HP (HubPeeker).

Makes sense? Trust me! ,,ԾㅂԾ,,

Again, email (check profile) can be used to ask for further explanation. (⊙_⊙;)
