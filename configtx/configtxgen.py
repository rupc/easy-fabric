#!/usr/bin/python3

import yaml
from string import Template
from argparse import ArgumentParser

def generate_config(num_orgs, num_orderers):
    # Base template for the YAML configuration
    base_template = """
Organizations:
  - &OrdererOrg
    Name: OrdererOrg
    ID: OrdererMSP
    MSPDir: ../../organizations/ordererOrganizations/example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('OrdererMSP.member')"
      Writers:
        Type: Signature
        Rule: "OR('OrdererMSP.member')"
      Admins:
        Type: Signature
        Rule: "OR('OrdererMSP.admin')"
    OrdererEndpoints:
$orderer_endpoints

$org_definitions

Capabilities:
  Channel: &ChannelCapabilities
    V2_0: true
  Orderer: &OrdererCapabilities
    V2_0: true
  Application: &ApplicationCapabilities
    V2_5: true

Application: &ApplicationDefaults
  Organizations:
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "ANY Admins"
    LifecycleEndorsement:
      Type: ImplicitMeta
      Rule: "ANY Endorsement"
    Endorsement:
      Type: ImplicitMeta
      Rule: "ANY Endorsement"
  Capabilities:
    <<: *ApplicationCapabilities

Orderer: &OrdererDefaults
  Addresses:
$orderer_addresses
  BatchTimeout: 2s
  BatchSize:
    MaxMessageCount: 100
    AbsoluteMaxBytes: 99 MB
    PreferredMaxBytes: 4 MB
  Organizations:
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "ANY Admins"
    BlockValidation:
      Type: ImplicitMeta
      Rule: "ANY Writers"

Channel: &ChannelDefaults
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "ANY Admins"
  Capabilities:
    <<: *ChannelCapabilities

Profiles:
  ChannelUsingRaft:
    <<: *ChannelDefaults
    Consortiums:
      SampleConsortium:
        Organizations:

    Orderer:
      <<: *OrdererDefaults
      OrdererType: etcdraft
      EtcdRaft:
        Consenters:
$consenters
      Organizations:
        - *OrdererOrg
      Capabilities: *OrdererCapabilities
    Application:
      <<: *ApplicationDefaults
      Organizations:
$profile_orgs
      Capabilities: *ApplicationCapabilities
"""

    # Create orderer endpoints and addresses
    orderer_endpoints = "\n".join([f"      - orderer{i+1}.example.com:7050" for i in range(num_orderers)])
    orderer_addresses = "\n".join([f"    - orderer{i+1}.example.com:7050" for i in range(num_orderers)])
    consenters = "\n".join([f"          - Host: orderer{i+1}.example.com\n            Port: 7050\n            ClientTLSCert: ../../organizations/ordererOrganizations/example.com/orderers/orderer{i+1}.example.com/tls/server.crt\n            ServerTLSCert: ../../organizations/ordererOrganizations/example.com/orderers/orderer{i+1}.example.com/tls/server.crt"
        for i in range(num_orderers)
    ])

    # Create organization definitions
    org_definitions = "\n".join([
        f"""  - &Org{i+1}
    Name: Org{i+1}MSP
    ID: Org{i+1}MSP
    MSPDir: ../../organizations/peerOrganizations/org{i+1}.example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('Org{i+1}MSP.admin', 'Org{i+1}MSP.peer', 'Org{i+1}MSP.client')"
      Writers:
        Type: Signature
        Rule: "OR('Org{i+1}MSP.admin', 'Org{i+1}MSP.client')"
      Admins:
        Type: Signature
        Rule: "OR('Org{i+1}MSP.admin')"
      Endorsement:
        Type: Signature
        Rule: "OR('Org{i+1}MSP.peer')" """
        for i in range(num_orgs)
    ])

    # application_orgs = "\n".join([f"  - *Org{i+1}" for i in range(num_orgs)])
    profile_orgs = "\n".join([f"        - *Org{i+1}" for i in range(num_orgs)])

    # Fill the template
    full_template = Template(base_template)
    yaml_content = full_template.substitute(
        orderer_endpoints=orderer_endpoints,
        org_definitions=org_definitions,
        orderer_addresses=orderer_addresses,
        # application_orgs=application_orgs,
        orderer_orgs="- *OrdererOrg",
        consenters=consenters,
        profile_orgs=profile_orgs
    )

    return yaml_content

import os
def main():
    parser = ArgumentParser(description="Generate a Fabric configuration YAML file with dynamic number of orgs and orderers.")
    parser.add_argument("--num_orgs", type=int, required=True, help="Number of organizations")
    parser.add_argument("--num_orderers", type=int, required=True, help="Number of orderers")
    args = parser.parse_args()

    # Generate and print the YAML content
    yaml_content = generate_config(args.num_orgs, args.num_orderers)
    
    configtxPath = f"configtx-{args.num_orgs}orgs-{args.num_orderers}orderers"
    filename = f"configtx.yaml"

    if not os.path.exists(configtxPath):
      os.makedirs(configtxPath)
      print(f"Directory created: {configtxPath}")
    
    # 파일 경로 결합
    file_path = os.path.join(configtxPath, filename)
    
    # 파일 쓰기
    with open(file_path, 'w') as file:
        file.write(yaml_content)
        print(f"File written: {file_path}")
    # print(yaml_content)

if __name__ == "__main__":
    main()
