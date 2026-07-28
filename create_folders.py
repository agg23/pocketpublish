#!/usr/bin/env python3

"""Create local directories to prepare for creating a release.

This assumes it's running in a GitHub action with various GITHUB_* env vars.
"""

import argparse
import sys

from helpers import *


def main(argv: list[str]) -> int | None:
    parser = argparse.ArgumentParser(description=__doc__)
    _opts = parser.parse_args(argv)

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


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
