#!/usr/bin/env python3
"""
********************************************************************************
* SPDX-License-Identifier: MIT
* SPDX-FileType: OTHER
* SPDX-FileCopyrightText: (c) 2024, OpenGateware authors and contributors
********************************************************************************
*
* Analogue Pocket Release Workflow
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

from helpers import *


def main():
    print("Starting")
    # Load gateware.json file
    config = read_gateware_json()
    # Compile design
    # run_quartus_compile(config)
    # Create base folders
    create_folders(config)
    # Copy package folders and files
    copy_packaging_folder(config)
    # Clean up unwanted files
    clean_up_files(config)
    # Update core release date and version
    update_apf_core_json(config)
    # Reverse Bitstream
    reverse_bitstream(config)
    # Create zip files for distribution
    pkg_file = create_release_package(config)
    meta_file = create_metadata_package(config)
    # Create GitHub release
    release_urls = create_gh_release(config, [pkg_file, meta_file])
    # Send Discord announcement
    # send_discord_announcement(config, release_urls)


if __name__ == '__main__':
    main()
