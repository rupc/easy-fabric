#!/usr/bin/python3

import yaml
from argparse import ArgumentParser


# Parse command line arguments for the number of organizations
# parser = ArgumentParser(description="Dynamically adjust the number of Orgs in a Fabric config template.")
# parser.add_argument("--org_count", type=int, help="Number of organizations to be included in the configuration.", required=True)
# args = parser.parse_args()

template_yaml_content = """
Organizations:
  - &OrdererOrg
    Name: OrdererOrg
    ID: OrdererMSP
    MSPDir: ../organizations/ordererOrganizations/example.com/msp
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
      - orderer1.example.com:7050
      - orderer2.example.com:7052
      - orderer3.example.com:7056
      - orderer4.example.com:7058
  - &Org1
    Name: Org1MSP
    ID: Org1MSP
    MSPDir: ../organizations/peerOrganizations/org1.example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('Org1MSP.admin', 'Org1MSP.peer', 'Org1MSP.client')"
      Writers:
        Type: Signature
        Rule: "OR('Org1MSP.admin', 'Org1MSP.client')"
      Admins:
        Type: Signature
        Rule: "OR('Org1MSP.admin')"
      Endorsement:
        Type: Signature
        Rule: "OR('Org1MSP.peer')"
  - &Org2
    Name: Org2MSP
    ID: Org2MSP
    MSPDir: ../organizations/peerOrganizations/org2.example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('Org2MSP.admin', 'Org2MSP.peer', 'Org2MSP.client')"
      Writers:
        Type: Signature
        Rule: "OR('Org2MSP.admin', 'Org2MSP.client')"
      Admins:
        Type: Signature
        Rule: "OR('Org2MSP.admin')"
      Endorsement:
        Type: Signature
        Rule: "OR('Org2MSP.peer')"
Capabilities:
  Channel: &ChannelCapabilities
    V3_0: true
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
      Rule: "MAJORITY Admins"
    LifecycleEndorsement:
      Type: ImplicitMeta
      Rule: "MAJORITY Endorsement"
    Endorsement:
      Type: ImplicitMeta
      Rule: "MAJORITY Endorsement"
  Capabilities:
    <<: *ApplicationCapabilities
Orderer:
  &OrdererDefaults # Batch Timeout: The amount of time to wait before creating a batch
  BatchTimeout: 2s
  # Batch Size: Controls the number of messages batched into a block
  BatchSize:
    # Max Message Count: The maximum number of messages to permit in a batch
    MaxMessageCount: 800
    # Absolute Max Bytes: The absolute maximum number of bytes allowed for
    # the serialized messages in a batch.
    AbsoluteMaxBytes: 99 MB
    # Preferred Max Bytes: The preferred maximum number of bytes allowed for
    # the serialized messages in a batch. A message larger than the preferred
    # max bytes will result in a batch larger than preferred max bytes.
    PreferredMaxBytes: 4 MB
  # Organizations is the list of orgs which are defined as participants on
  # the orderer side of the network
  Organizations:
  # Policies defines the set of policies at this level of the config tree
  # For Orderer policies, their canonical path is
  #   /Channel/Orderer/<PolicyName>
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
    # BlockValidation specifies what signatures must be included in the block
    # from the orderer for the peer to validate it.
    BlockValidation:
      Type: ImplicitMeta
      Rule: "ANY Writers"
Channel: &ChannelDefaults
  # Policies defines the set of policies at this level of the config tree
  # For Channel policies, their canonical path is
  #   /Channel/<PolicyName>
  Policies:
    # Who may invoke the 'Deliver' API
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    # Who may invoke the 'Broadcast' API
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    # By default, who may modify elements at this config level
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
  # Capabilities describes the channel level capabilities, see the
  # dedicated Capabilities section elsewhere in this file for a full
  # description
  Capabilities:
    <<: *ChannelCapabilities
Profiles:
  ChannelUsingBFT:
    <<: *ChannelDefaults
    Orderer:
      <<: *OrdererDefaults
      Organizations:
        - *OrdererOrg
      Capabilities: *OrdererCapabilities
      OrdererType: BFT
      SmartBFT:
        RequestBatchMaxCount: 100
        RequestBatchMaxInterval: 50ms
        RequestForwardTimeout: 2s
        RequestComplainTimeout: 20s
        RequestAutoRemoveTimeout: 3m0s
        ViewChangeResendInterval: 5s
        ViewChangeTimeout: 20s
        LeaderHeartbeatTimeout: 1m0s
        CollectTimeout: 1s
        RequestBatchMaxBytes: 10485760
        IncomingMessageBufferSize: 200
        RequestPoolSize: 100000
        LeaderHeartbeatCount: 10
      ConsenterMapping:
        - ID: 1
          Host: orderer1.example.com
          Port: 7050
          MSPID: OrdererMSP
          Identity: ../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/msp/signcerts/orderer1.example.com-cert.pem
          ClientTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/server.crt
          ServerTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/server.crt
        - ID: 2
          Host: orderer2.example.com
          Port: 7052
          MSPID: OrdererMSP
          Identity: ../organizations/ordererOrganizations/example.com/orderers/orderer2.example.com/msp/signcerts/orderer2.example.com-cert.pem
          ClientTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer2.example.com/tls/server.crt
          ServerTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer2.example.com/tls/server.crt
        - ID: 3
          Host: orderer3.example.com
          Port: 7056
          MSPID: OrdererMSP
          Identity: ../organizations/ordererOrganizations/example.com/orderers/orderer3.example.com/msp/signcerts/orderer3.example.com-cert.pem
          ClientTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer3.example.com/tls/server.crt
          ServerTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer3.example.com/tls/server.crt
        - ID: 4
          Host: orderer4.example.com
          Port: 7058
          MSPID: OrdererMSP
          Identity: ../organizations/ordererOrganizations/example.com/orderers/orderer4.example.com/msp/signcerts/orderer4.example.com-cert.pem
          ClientTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer4.example.com/tls/server.crt
          ServerTLSCert: ../organizations/ordererOrganizations/example.com/orderers/orderer4.example.com/tls/server.crt
    Application:
      <<: *ApplicationDefaults
      Organizations:
        - *Org1
        - *Org2
      Capabilities: *ApplicationCapabilities
"""

org_count = 3
# org_count = args.org_count

data = yaml.safe_load(template_yaml_content)

# Function to create org definition
def create_org_definition(org_index):
    return {
        "Name": f"Org{org_index}MSP",
        "ID": f"Org{org_index}MSP",
        "MSPDir": f"../organizations/peerOrganizations/org{org_index}.example.com/msp",
        "Policies": {
            "Readers": {
                "Type": "Signature",
                "Rule": f"OR('Org{org_index}MSP.admin', 'Org{org_index}MSP.peer', 'Org{org_index}MSP.client')"
            },
            "Writers": {
                "Type": "Signature",
                "Rule": f"OR('Org{org_index}MSP.admin', 'Org{org_index}MSP.client')"
            },
            "Admins": {
                "Type": "Signature",
                "Rule": f"OR('Org{org_index}MSP.admin')"
            },
            "Endorsement": {
                "Type": "Signature",
                "Rule": f"OR('Org{org_index}MSP.peer')"
            }
        }
    }

# Adjust the number of orgs in the template
data["Organizations"] = data["Organizations"][:2]  # Keep the OrdererOrg, remove existing peer orgs
for i in range(1, org_count + 1):
    OrgDefinition = create_org_definition(i)
    data["Organizations"].append(create_org_definition(i))

# Adjust the number of orgs in the channel profile
data["Profiles"]["ChannelUsingBFT"]["Application"]["Organizations"] = []
for i in range(1, org_count + 1):
    data["Profiles"]["ChannelUsingBFT"]["Application"]["Organizations"].append({"*Org": f"Org{i}"})

# Save the modified template to a new file
with open(f"bftconfigtx_{org_count}_orgs.yaml", "w") as file:
    yaml.dump(data, file, sort_keys=False)

print(f"Configuration with {org_count} organizations generated successfully.")
