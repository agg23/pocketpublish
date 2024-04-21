#!/usr/bin/env python3
"""
********************************************************************************
* SPDX-License-Identifier: MIT
* SPDX-FileType: OTHER
* SPDX-FileCopyrightText: (c) 2024, OpenGateware authors and contributors
********************************************************************************
*
* OpenGateware Workflow Helpers
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

from .GitHubReleaseManager import *
from .release import *
from .discord import *
from .package import *
from .json import *

__all__ = [
    # JSON Helpers
    "read_json_file",
    "save_json_file",
    "read_gateware_json",
    "update_apf_core_json",
    # Package
    "create_folders",
    "copy_packaging_folder",
    "clean_up_files",
    "create_release_package",
    "create_metadata_package",
    "create_tar_gz",
    "create_zip_file",
    "reverse_bitstream",
    # Release
    "create_gh_release",
    "GitHubReleaseManager",
    # Discord
    "send_discord_announcement",
]
