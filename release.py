from helpers import *


def main():
    print("Releasing")
    # Load gateware.json file
    config = read_gateware_json()
    # Create zip files for distribution
    pkg_file = create_release_package(config)
    meta_file = create_metadata_package(config)
    # Create GitHub release
    release_urls = create_gh_release(config, [pkg_file, meta_file])
    # Send Discord announcement
    # send_discord_announcement(config, release_urls)


if __name__ == "__main__":
    main()
