#!/usr/bin/env python3

import yaml

peer_template = """
version: '3.7'
networks:
  test:
    name: fabric_test
services:
  peer{index}.org{OrgIndex}.example.com:
    container_name: peer{index}.org{OrgIndex}.example.com
    image: hyperledger/fabric-peer:2.5.6
    labels:
      service: hyperledger-fabric
    environment:
      - FABRIC_CFG_PATH=/etc/hyperledger/peercfg
      - FABRIC_LOGGING_SPEC=INFO
      #- FABRIC_LOGGING_SPEC=DEBUG
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=fabric_test
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_PROFILE_ENABLED=false
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/msp
      # - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp
      - CORE_PEER_ID=peer{index}.org{OrgIndex}.example.com
      - CORE_PEER_ADDRESS=peer{index}.org{OrgIndex}.example.com:7051
      - CORE_PEER_LISTENADDRESS=0.0.0.0:7051
      - CORE_PEER_CHAINCODEADDRESS=peer{index}.org{OrgIndex}.example.com:7052
      - CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:7052
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer0.org{OrgIndex}.example.com:7051
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer{index}.org{OrgIndex}.example.com:7051
      - CORE_PEER_GOSSIP_ORGLEADER=true
      - CORE_PEER_GOSSIP_USELEADERELECTION=false
      - CORE_PEER_LOCALMSPID=Org{OrgIndex}MSP
      - CORE_OPERATIONS_LISTENADDRESS=peer{index}.org{OrgIndex}.example.com:9444
      - CORE_METRICS_PROVIDER=prometheus
      - CHAINCODE_AS_A_SERVICE_BUILDER_CONFIG={{"peername":"peer{index}org{OrgIndex}"}}
      - CORE_CHAINCODE_EXECUTETIMEOUT=300s
    volumes:
      - ../organizations/peerOrganizations/org{OrgIndex}.example.com/peers/peer{index}.org{OrgIndex}.example.com:/etc/hyperledger/fabric
      - ../organizations/peerOrganizations/org{OrgIndex}.example.com/users/Admin@org{OrgIndex}.example.com/msp:/etc/hyperledger/fabric/adminmsp
      - ../organizations/peerOrganizations/:/etc/hyperledger/fabric/peerOrganizations
      - ../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/:/etc/hyperledger/fabric/orderercert
      - ./data/peer{index}.org{OrgIndex}.example.com:/var/hyperledger/production
      - ./config:/etc/hyperledger/peercfg
      - ../channel-artifacts:/etc/hyperledger/fabric/channel-artifacts
      - ../chaincode:/etc/hyperledger/fabric/chaincode
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /root
    command: peer node start
    ports:
      - {peer_port}:7051
      - {peer_ops_port}:9444
    networks:
      - test
"""

orderer_template = """
version: '3.7'
networks:
  test:
    name: fabric_test
services:
  orderer{index}.example.com:
    container_name: orderer{index}.example.com
    image: hyperledger/fabric-orderer:2.5.6
    labels:
      service: hyperledger-fabric
    environment:
      - FABRIC_LOGGING_SPEC=INFO
    #   - ORDERER_GENERAL_GENESISMETHOD=file
    #   - ORDERER_GENERAL_GENESISFILE=/var/hyperledger/orderer/orderer.genesis.block
      - ORDERER_GENERAL_BOOTSTRAPMETHOD=file
      - ORDERER_GENERAL_BOOTSTRAPFILE=/var/hyperledger/orderer/orderer.genesis.block
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_LISTENPORT=7050
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
      - ORDERER_GENERAL_TLS_ENABLED=true
      - ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_GENERAL_CLUSTER_CLIENTCERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_CLUSTER_CLIENTPRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_CLUSTER_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_CHANNELPARTICIPATION_ENABLED=true
      - ORDERER_ADMIN_TLS_ENABLED=true
      - ORDERER_ADMIN_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_ADMIN_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_ADMIN_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_ADMIN_LISTENADDRESS=0.0.0.0:7053
      - ORDERER_OPERATIONS_LISTENADDRESS=orderer{index}.example.com:9443
      - ORDERER_METRICS_PROVIDER=prometheus
    working_dir: /root
    command: orderer
    volumes:
      - ../organizations/ordererOrganizations/example.com/orderers/orderer{index}.example.com/msp:/var/hyperledger/orderer/msp
      - ../organizations/ordererOrganizations/example.com/orderers/orderer{index}.example.com/tls/:/var/hyperledger/orderer/tls
      - ../organizations/ordererOrganizations/example.com/users/Admin@example.com/msp:/var/hyperledger/orderer/adminmsp
      - ../organizations/ordererOrganizations/example.com/tlsca:/var/hyperledger/orderer/tlsca
      - ./data/orderer{index}.example.com:/var/hyperledger/production/orderer
      - ../channel-artifacts/genesis.block:/var/hyperledger/orderer/orderer.genesis.block
      - ../../bin:/var/hyperledger/bin
    ports:
      - {orderer_port}:7050
      - {orderer_admin_port}:7053
      - {orderer_ops_port}:9443
    networks:
      - test
"""


def generate_yaml_files(num_peers, num_orderers, peer_template, orderer_template):
    peer_port = 7051  # 외부로 노출되는 Peer 포트 시작 번호
    peer_ops_port = 9444
    orderer_port = 7050  # 외부로 노출되는 Orderer 포트 시작 번호
    orderer_admin_port = 7053  # 외부로 노출되는 Orderer 포트 시작 번호
    orderer_ops_port = 9443  # 외부로 노출되는 Orderer 포트 시작 번호

    peers_combined = {'version': '3.7', 'networks': {'test': {'name': 'fabric_test'}}, 'services': {}}
    orderers_combined = {'version': '3.7', 'networks': {'test': {'name': 'fabric_test'}}, 'services': {}}

 
    # Generate peer YAML files
    for i in range(num_peers):
        file_name = f"peer{0}.org{i+1}.yaml"
        # file_name = f"peer{i+1}.org1.yaml"
        peer_port += 10
        peer_ops_port += 10
        content = peer_template.format(index=0, OrgIndex=i+1, peer_port=peer_port, peer_ops_port=peer_ops_port)
 
        with open(file_name, "w") as file:
            file.write(content)
        peers_combined['services'][f'peer{0}.org{i+1}.example.com'] = yaml.safe_load(content.split('services:\n')[1].split('\n\n')[0])[f'peer{0}.org{i+1}.example.com']
        # peers_combined['services'][f'peer{i}.org{i}.example.com'] = yaml.safe_load(content.split('services:\n')[1].split('\n\n')[0])[f'peer{i}.org1.example.com']
 

    # Generate orderer YAML files
    for i in range(num_orderers):
        file_name = f"orderer{i+1}.yaml"
        orderer_port += 10
        orderer_admin_port += 10
        orderer_ops_port += 10
        content = orderer_template.format(index=i+1, orderer_port=orderer_port, orderer_admin_port=orderer_admin_port, orderer_ops_port=orderer_ops_port)
        # content = orderer_template.format(index=i+1, orderer_port=orderer_port, orderer_admin_port=orderer_admin_port, orderer_ops_port=orderer_ops_port)
 
        with open(file_name, "w") as file:
            file.write(content)
        # orderers_combined['services'][f'orderer{i+1}.example.com'] = yaml.safe_load(content.split('services:\n')[1].split('\n\n')[0])
        orderers_combined['services'][f'orderer{i+1}.example.com'] = yaml.safe_load(content.split('services:\n')[1].split('\n\n')[0])[f'orderer{i+1}.example.com']
        

 
     # Write combined peers.yaml
    with open('peers.yaml', 'w') as file:
        yaml.dump(peers_combined, file)
        
    # Write combined orderers.yaml
    with open('orderers.yaml', 'w') as file:
        yaml.dump(orderers_combined, file)



# Read the bench-config.yaml
with open('bench-config.yaml', 'r') as file:
    config = yaml.safe_load(file)

num_peers = config['General']['NumPeers']
num_orderers = config['General']['NumOrderers']

# Define the peer and orderer templates


# Generate YAML files based on the configuration
generate_yaml_files(num_peers, num_orderers, peer_template, orderer_template)
