#!/usr/bin/python3
import argparse

def generate_yaml_files(num_orgs, num_orderers):
    peer_orgs = []
    orderer_orgs = []

    # Generate Peer Organizations
    for i in range(1, num_orgs + 1):
        peer_org = f"""
  - Name: Org{i}
    Domain: org{i}.example.com
    EnableNodeOUs: true
    Template:
      Count: 1
      SANS:
        - localhost
    Users:
      Count: 1
"""
        peer_orgs.append(peer_org)

    # Write to Peer Organizations YAML file
    peer_yaml_content = "PeerOrgs:\n" + "".join(peer_orgs)
    peer_file_name = f"crypto-config-{num_orgs}-org.yaml"
    with open(peer_file_name, 'w') as file:
        file.write(peer_yaml_content)
    print(f"YAML file '{peer_file_name}' has been created for peer organizations.")
        # Generate Orderer Organizations
    
    orderer_specs = "".join([f"""
      - Hostname: orderer{i}
        SANS:
          - localhost""" for i in range(1, num_orderers + 1)
    ])
    
    orderer_org = f"""
  - Name: Orderer
    Domain: example.com
    EnableNodeOUs: true
    Specs:
{orderer_specs}
"""
    yaml_content = f"""
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
---
OrdererOrgs:
{orderer_org}
"""
    print(orderer_org)
    # Write to Orderer Organizations YAML file
    # orderer_yaml_content = "OrdererOrgs:\n" + "".join(orderer_orgs)
    orderer_file_name = f"crypto-config-{num_orderers}-orderer.yaml"
    with open(orderer_file_name, 'w') as file:
        file.write(yaml_content)

    # with open(orderer_file_name, 'w') as file:
    #     file.write(orderer_yaml_content)
    print(f"YAML file '{orderer_file_name}' has been created for orderer organizations.")

def main():
    parser = argparse.ArgumentParser(description='Generate YAML configuration for Hyperledger Fabric network setup.')
    parser.add_argument('--num_orgs', type=int, required=True, help='Number of peer organizations')
    parser.add_argument('--num_orderers', type=int, required=True, help='Number of orderer nodes')
    
    args = parser.parse_args()
    
    generate_yaml_files(args.num_orgs, args.num_orderers)

if __name__ == "__main__":
    main()
