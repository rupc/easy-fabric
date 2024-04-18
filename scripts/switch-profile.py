#!/usr/bin/python3

import argparse
import shutil
import os

def main():
    parser = argparse.ArgumentParser(description="Generate the necessary files for a specific HLF profile.")
    parser.add_argument("--profile", choices=[
        "12orgs-3orderers",
        "24orgs-6orderers",
        "36orgs-9orderers",
        "48orgs-12orderers",
        "60orgs-15orderers"
    ], required=True, help="Specify the profile to setup.")

    args = parser.parse_args()

    # Map the profile to the directory name and genesis block name
    dir_map = {
        "12orgs-3orderers": "12orgs-3orderers",
        "24orgs-6orderers": "24orgs-6orderers",
        "36orgs-9orderers": "36orgs-9orderers",
        "48orgs-12orderers": "48orgs-12orderers",
        "60orgs-15orderers": "60orgs-15orderers"
    }

    # Define the paths
    organizations_path = "../organizations"
    cryptogen_path = f"../cryptogen/organizations-{args.profile}"
    genesis_block_src = f"../channel-artifacts/{dir_map[args.profile]}.genesis.block"
    genesis_block_dst = "../channel-artifacts/genesis.block"

    # Remove the existing organizations directory
    if os.path.exists(organizations_path):
        shutil.rmtree(organizations_path)
    
    # Copy the specific profile's organizations directory
    shutil.copytree(cryptogen_path, organizations_path)

    # Move the genesis block to the required location
    shutil.copy(genesis_block_src, genesis_block_dst)

    print(f"Setup for profile {args.profile} completed successfully.")

if __name__ == "__main__":
    main()
