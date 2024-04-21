"""
********************************************************************************
* SPDX-License-Identifier: MIT
* SPDX-FileType: OTHER
* SPDX-FileCopyrightText: (c) 2024, OpenGateware authors and contributors
********************************************************************************
*
* Intel Quartus Compilation Flow
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

import json
import mimetypes
import os
import requests
import subprocess


class GitHubReleaseManager:
    def __init__(self, config, token):
        """
        Initializes the GitHubReleaseManager with repository and token.

        Parameters:
        - repo (str): The repository name in the format 'username/repo'.
        - token (str): Personal access token for GitHub API authentication.
        """
        self.config = config
        self.repo = f'{os.getenv("GITHUB_REPOSITORY")}'
        self.tag = f'{os.getenv("GITHUB_REF_NAME")}'
        self.token = f'{os.getenv("GH_TOKEN")}'
        self.gh_url = os.getenv("GITHUB_API_URL")
        self.release_url = f"{self.gh_url}/repos/{self.repo}/releases"
        self.release_folder = self.config['release']['folders']['release_folder']
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    @staticmethod
    def get_current_git_branch():
        """
        Retrieves the current Git branch name.

        Returns:
        - str: The current branch name if successful, None otherwise.
        """
        try:
            # Run the git command to get the current branch name
            branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode('utf-8')
            return branch_name
        except subprocess.CalledProcessError:
            # Handle errors if Git command fails
            print("An error occurred while trying to fetch the current Git branch.")
            return None

    @staticmethod
    def get_mime_type(filename):
        """
        Returns the MIME type for a given filename based on its extension.

        Parameters:
        - filename (str): The name of the file.

        Returns:
        - str: The guessed MIME type of the file. Returns 'application/octet-stream' if the MIME type cannot be guessed.
        """
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type if mime_type else 'application/octet-stream'

    def release_exists(self, tag_name):
        """
         Checks if a release with the specified tag name exists.

         Parameters:
         - tag_name (str): The tag name of the release to check.

         Returns:
         - tuple: (bool, dict) - True if release exists along with the release info, False and empty dict otherwise.

         Throws:
         - Exception: If there's an issue querying the GitHub API.
         """
        response = requests.get(self.release_url, headers=self.headers)
        if response.status_code == 200:
            releases = response.json()
            for release in releases:
                if release['tag_name'] == tag_name:
                    return True, release
            return False, {}
        else:
            raise Exception(f"Error querying releases: {response.content}")

    def create_release(self, tag_name):
        """
        Creates a new release on GitHub.

        Parameters:
        - tag_name (str): The tag name for the new release.

        Returns:
        - dict: The response from GitHub API for the newly created release.

        Throws:
        - Exception: If there's an error creating the release via the GitHub API.
        """
        payload = {
            "tag_name": tag_name,
            "target_commitish": self.get_current_git_branch(),
            "name": f"Release v{tag_name}",
            "body": f"Release v{tag_name}",
            "draft": False,
            "prerelease": False
        }
        response = requests.post(self.release_url, headers=self.headers, data=json.dumps(payload))
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error creating release: {response.content}")

    def get_upload_url(self):
        """
        Retrieves the upload URL for a release's assets.

        Returns:
        - str: The upload URL for the release's assets.
        """
        exists, response = self.release_exists(self.tag)
        if exists:
            print("Release Already Exists...")
            return response['upload_url']
        else:
            print("Creating New Release...")
            release = self.create_release(self.tag)
            return release['upload_url']
        pass

    def upload_asset(self, upload_url, file_path, content_type):
        """
        Uploads an asset to a given release.

        Parameters:
        - upload_url (str): The URL for uploading assets to the release.
        - file_path (str): The local path to the file to be uploaded.
        - content_type (str): The MIME type of the file being uploaded.

        Returns:
        - dict: The response from GitHub API for the uploaded asset.

        Throws:
        - Exception: If there's an error uploading the asset via the GitHub API.
        """
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": content_type
        }
        with open(file_path, 'rb') as file:
            response = requests.post(upload_url, headers=headers, data=file)
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error uploading asset: {response.content}")

    def create_gh_release(self, files):
        """
        Creates a GitHub release and uploads specified files as assets.

        Parameters:
        - config (dict): Configuration details for the release, including the release folder path.
        - files (list of str): Filenames of the assets to be uploaded.

        Returns:
        - list of str: Browser download URLs for the uploaded assets.
        """
        download_urls = []
        upload_url = self.get_upload_url()

        for release_file in files:
            asset_upload_url = upload_url.replace("{?name,label}", f"?name={release_file}")
            file_path = f'{self.release_folder}/{release_file}'
            content_type = self.get_mime_type(file_path)
            asset_info = self.upload_asset(asset_upload_url, file_path, content_type)
            if 'browser_download_url' in asset_info:
                download_urls.append(asset_info['browser_download_url'])

        return download_urls

# # Example usage:
# repo = "your_username/your_repo"
# token = "your_github_token"
# release_manager = GitHubReleaseManager(repo, token)
#
# # Assuming you have defined the methods' contents, you could use them like this:
# branch = release_manager.get_current_git_branch()
# if not release_manager.release_exists("v1.0.0"):
#     release_manager.create_release("v1.0.0")
