#!/usr/bin/env python3

"""Generate release artifacts.

This assumes it's running in a GitHub action with various GITHUB_* env vars.
"""

import argparse
import sys

from helpers import *


def main(argv: list[str]) -> int | None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--norelease", action="store_true", required=False)
    opts = parser.parse_args(argv)

    print("Releasing")
    # Load gateware.json file
    config = read_gateware_json()
    # Create zip files for distribution
    pkg_file = create_release_package(config, "pocket")
    meta_file = create_metadata_package(config, "pocket")
    # Create GitHub release
    if not opts.norelease:
        release_urls = create_gh_release(config, [pkg_file, meta_file])
    # Send Discord announcement
    # send_discord_announcement(config, release_urls)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
