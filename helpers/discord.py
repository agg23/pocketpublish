"""
********************************************************************************
* SPDX-License-Identifier: MIT
* SPDX-FileType: OTHER
* SPDX-FileCopyrightText: (c) 2024, OpenGateware authors and contributors
********************************************************************************
*
* Discord Announcements
* Copyright (c) 2024, Marcus Andrade <marcus@opengateware.org>
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
********************************************************************************
"""

import os
import requests
import json


def get_platform_name(target, board=None):
    """
    Determines the platform name based on the given target identifier.

    Parameters:
    - target (str): The target platform identifier (e.g., "pocket", "mimic", "deca").

    Returns:
    - str: A human-readable name for the platform.
    """
    match target:
        case "mimic":
            return f"MiMiC NSX for {board}"
        case "pocket":
            return "Analogue Pocket"
        case "mist":
            return "MiST"
        case "sidi":
            return "SiDi"
        case "mister":
            return "MiSTer"
        case "neptuno":
            return "NeptUNO"
        case "cyc1000":
            return "Trenz CYC1000"
        case "deca":
            return "Arrow DECA"
        case "tc64v1":
            return "Turbo Chameleon 64 v1"
        case "tc64v2":
            return "Turbo Chameleon 64 v2"


def get_github_user_avatar_url(username):
    """
    Fetches the avatar URL of a GitHub user.

    Parameters:
    - username: GitHub username of the user whose avatar URL you want to fetch.

    Returns:
    - The avatar URL if the user exists and the request was successful.
    - None if the user does not exist or the request failed.
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('avatar_url')
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None


def format_download_links(urls):
    """
    Formats a list of URLs as Markdown links with filenames as the link text.

    Parameters:
    - urls (list of str): A list of URLs to format.

    Returns:
    - str: A string containing Markdown-formatted links, one per line.
    """
    # Initialize an empty string to hold the formatted download links
    download_links = ""

    for url in urls:
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        # Append the Markdown link for this file to the download_links string
        download_links += f"- [{filename}]({url})\n"

    return download_links


def send_discord_announcement(config, files):
    """
    Sends an announcement to Discord via webhooks.

    Constructs a Discord message embed containing details about a release,
    including title, description, platform, version, category, and download links,
    and sends this message to all Discord webhooks prefixed with "WEBHOOK_" found in environment variables.

    Parameters:
    - config (dict): A dictionary containing configuration and release details.
    - files (list of str): A list of file URLs to include in the download section of the announcement.

    Side Effects:
    - Sends a POST request to each Discord webhook URL found in environment variables.

    Raises:
    - Exception: If any Discord webhook POST request fails.
    """
    print("Preparing to send Discord Announcements...")

    # Filter out invalid or empty URLs from the files list
    valid_files = [url for url in files if url and isinstance(url, str)]

    # If no valid download URLs, skip sending the announcement
    if not valid_files:
        print("No valid download URLs found. Skipping Discord announcement.")
        return

    # Prepare the announcement content
    repo = f'{os.getenv("GITHUB_REPOSITORY")}'
    version = f'{os.getenv("GITHUB_REF_NAME")}'
    platform = get_platform_name(f'{os.getenv("TARGET")}')

    title = config['displayName']
    description = config['description']
    author = config['author']
    avatar = get_github_user_avatar_url(author)
    developer = f"[{author}](https://github.com/{author})"
    category = config['hardware']['category']
    image = f"https://github.com/{repo}/raw/master/{config['release']['image']}"
    links = (f"- [Repository](https://github.com/{repo}/)\n"
             f"- [Release](https://github.com/{repo}/releases/tag/{version})")
    download = format_download_links(valid_files)

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "username": f"{author}",
        "avatar_url": f"{avatar}",
        "embeds": [{
            "color": 2021216,
            "title": f"{title}",
            "image": {"url": f"{image}"},
            "fields": [
                {"name": "Platform", "value": f"{platform}", "inline": True},
                {"name": "Version", "value": f"{version}", "inline": True},
                {"name": "Category", "value": f"{category}", "inline": True},
                {"name": "Description", "value": f"{description}"},
                {"name": "Developer", "value": f"{developer}"},
                {"name": "Links", "value": f"{links}"},
                {"name": "Download", "value": f"{download}"},
            ]
        }]
    }

    # Find all environment variables that start with the prefix "WEBHOOK_"
    prefix = "WEBHOOK_"
    webhook_env_vars = {key: value for key, value in os.environ.items() if key.startswith(prefix)}

    # Dispatch message to each webhook
    for server, webhook in webhook_env_vars.items():
        if webhook:
            try:
                print(f"Sending announcement to {server.removeprefix(prefix).lower()}...")
                response = requests.post(webhook, headers=headers, data=json.dumps(data))
                if response.status_code != 204:
                    print(f"Error sending Discord notification: {response.content}")
                else:
                    print(f"Announcement sent successfully to {server.removeprefix(prefix).lower()}.")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send message due to an error: {e}")
        else:
            print(f"No valid webhook detected for {server.removeprefix(prefix).lower()}")
