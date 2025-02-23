from helpers import *
import argparse


def main():
    print("Releasing")
    parser = argparse.ArgumentParser()
    parser.add_argument("--norelease", action="store_true", required=False)
    args = parser.parse_args()
    # Load gateware.json file
    config = read_gateware_json()
    # Create zip files for distribution
    pkg_file = create_release_package(config, "pocket")
    meta_file = create_metadata_package(config, "pocket")
    # Create GitHub release
    if not args.norelease:
        release_urls = create_gh_release(config, [pkg_file, meta_file])
    # Send Discord announcement
    # send_discord_announcement(config, release_urls)


if __name__ == "__main__":
    main()
