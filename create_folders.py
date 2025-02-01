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


if __name__ == "__main__":
    main()
