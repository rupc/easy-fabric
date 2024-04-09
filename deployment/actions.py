#!/usr/bin/python3 
import subprocess
import yaml 
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# argparse를 사용하여 커맨드 라인 인자 처리
parser = argparse.ArgumentParser(description='Manage chaincode on Fabric network.')
parser.add_argument('action', type=str, choices=['join', 'install', 'instan', 'approve','commit'], help='Action to perform: join, install, or instan')
args = parser.parse_args()

# Read the bench-config.yaml
with open('bench-config.yaml', 'r') as file:
    config = yaml.safe_load(file)


bin_path = "../../bin"

# 채널 구성 블록 파일의 경로

# CLI 컨테이너 이름
cli_container_name = "peer0.org1.example.com"
# cli_container_name = "cli"

# 조인할 채널 이름
channel_name = "mychannel"

# MSP 구성 경로와 TLS 인증서 경로를 설정하세요.
# ../organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
channel_block_path = "/etc/hyperledger/fabric/channel-artifacts/genesis.block"
channel_creation_path = "/etc/hyperledger/fabric/channel-artifacts/mychannel.tx"

admin_msp_config_path = "/etc/hyperledger/fabric/adminmsp/"
# tls_root_cert_path = "/etc/hyperledger/fabric/msp"
# /etc/hyperledger/fabric/tls/ca.crt

# 조인할 피어의 수
peer_count = config['General']['NumPeers']
orderer_count = config['General']['NumOrderers']

# 조인할 피어의 도메인
org_domain = "org1.example.com"
def createchannel():
    pass
    # for i in range(peer_count):
    #     orderer4.example.com
    # orderer_address = f"orderer{i+1}.example.com:7050"
    # tls_root_cert_file = f"/etc/hyperledger/fabric/tls/ca.crt"
    # # tls_root_cert_file = f"{tls_root_cert_path}/peer{i}.{org_domain}/tls/ca.crt"
    # cli_container_name = f"peer{0}.org{i+1}.example.com"
    
# osnadmin channel join --channelID channel1 --config-block genesis_block.pb -o OSN1.example.com:7050 --ca-file $OSN_TLS_CA_ROOT_CERT --client-cert $ADMIN_TLS_SIGN_CERT --client-key $ADMIN_TLS_PRIVATE_KEY


# export OSN_TLS_CA_ROOT_CERT=.organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/cacerts/tls-ca-cert.pem
# export ADMIN_TLS_SIGN_CERT=.admin-client/client-tls-cert.pem
# export ADMIN_TLS_PRIVATE_KEY=.admin-client/client-tls-key.pem

# osnadmin channel join --channelID [CHANNEL_NAME]  --config-block [CHANNEL_CONFIG_BLOCK] -o [ORDERER_ADMIN_LISTENADDRESS] --ca-file $OSN_TLS_CA_ROOT_CERT --client-cert $ADMIN_TLS_SIGN_CERT --client-key $ADMIN_TLS_PRIVATE_KEY

    pass
    
def join_peers():
    for i in range(peer_count):
        peer_address = f"peer{0}.org{i+1}.example.com:7051"
        tls_root_cert_file = f"/etc/hyperledger/fabric/tls/ca.crt"
        # tls_root_cert_file = f"{tls_root_cert_path}/peer{i}.{org_domain}/tls/ca.crt"
        cli_container_name = f"peer{0}.org{i+1}.example.com"

        # Docker exec 명령어 구성
        docker_exec_cmd = [
            "docker", "exec",
            cli_container_name,
            "env", f"CORE_PEER_ADDRESS={peer_address}",
            f"CORE_PEER_TLS_ROOTCERT_FILE={tls_root_cert_file}",
            f"CORE_PEER_LOCALMSPID=Org{i+1}MSP",
            f"CORE_PEER_MSPCONFIGPATH={admin_msp_config_path}",
            "peer", "channel", "join", "-b", channel_block_path
        ]

        # 명령어 실행
        result = subprocess.run(docker_exec_cmd, capture_output=True, text=True)
        
        # 결과 출력
        if result.returncode == 0:
            print(f"Peer {peer_address} successfully joined {channel_name}.")
        else:
            print(f"Failed to join peer {peer_address} to {channel_name}. Error: {result.stderr}")

# def package():
    
chaincode_name = "smallbank"
chaincode_version = "v1.0"

def install_cc():
    package_file = f"{chaincode_name}_{chaincode_version}.tar.gz"
    package_path = "/etc/hyperledger/fabric/chaincode/"
    for i in range(peer_count):
        peer_address = f"peer{0}.org{i+1}.example.com:7051"
        tls_root_cert_file = f"/etc/hyperledger/fabric/tls/ca.crt"
        install_command = [
            "docker", "exec",
            peer_address.split(":")[0],
            "env", f"CORE_PEER_ADDRESS={peer_address}",
            f"CORE_PEER_TLS_ROOTCERT_FILE={tls_root_cert_file}",
            f"CORE_PEER_LOCALMSPID=Org{i+1}MSP",
            f"CORE_PEER_MSPCONFIGPATH={admin_msp_config_path}",
            "peer", "lifecycle", "chaincode", "install", package_path+package_file
        ]

        result = subprocess.run(install_command, capture_output=True, text=True)
            
        if result.returncode == 0:
            print(f"Chaincode installed successfully on {peer_address}.")
        else:
            print(f"Error installing chaincode on {peer_address}: {result.stderr}")


# peer lifecycle chaincode commit -o orderer.example.com:7050 --channelID mychannel --name smallbank --version 1.0 --sequence 1 --tls true --cafile $ORDERER_CA --signature-policy "AND('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer','Org4MSP.peer')"

def instantiate_cc():
    print("Instantiating chaincode...")
    # 여기에 instantiate_cc() 함수의 로직을 추가하세요.
    # 이 예시에서는 이 함수의 구현을 생략하고 있습니다.
    pass

# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode approveformyorg --channelID mychannel --name smallbank --version 1.0 --sequence 1 --package-id smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050
# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode commit  --channelID mychannel --name smallbank --version 1.0 --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050 --signature-policy "OR('Org1MSP.peer')"
# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode commit  --channelID mychannel --name smallbank --version 1.0 --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050


# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode approveformyorg --channelID mychannel --name smallbank --version 1.0 --package-id smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13 --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050 --signature-policy "AND('Org1MSP.peer', 'Org2MSP.peer', 'Org3MSP.peer', 'Org4MSP.peer', 'Org5MSP.peer', 'Org6MSP.peer', 'Org7MSP.peer', 'Org8MSP.peer', 'Org9MSP.peer', 'Org10MSP.peer', 'Org11MSP.peer', 'Org12MSP.peer')"


# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode queryapproved --channelID mychannel --name smallbank --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt
# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode queryinstalled


endorsement_policy = "OutOf(4, 'Org1MSP.peer', 'Org2MSP.peer', 'Org3MSP.peer', 'Org4MSP.peer', 'Org5MSP.peer', 'Org6MSP.peer', 'Org7MSP.peer', 'Org8MSP.peer', 'Org9MSP.peer', 'Org10MSP.peer', 'Org11MSP.peer', 'Org12MSP.peer')"
def approve():
    # package_id = "smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13"  # 승인할 체인코드 패키지 ID
    package_id = "smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13"  # 승인할 체인코드 패키지 ID

    print(package_id)
    # 승인 명령 구성
    for i in range(peer_count):
        peer_address = f"peer{0}.org{i+1}.example.com:7051"
        print("approve for", peer_address.split(":")[0])
        tls_root_cert_file = f"/etc/hyperledger/fabric/tls/ca.crt"
        command = [
            "docker", "exec", 
            peer_address.split(":")[0],
            "env", f"CORE_PEER_ADDRESS={peer_address}",
            f"CORE_PEER_TLS_ROOTCERT_FILE={tls_root_cert_file}",
            f"CORE_PEER_LOCALMSPID=Org{i+1}MSP",
            f"CORE_PEER_MSPCONFIGPATH={admin_msp_config_path}",
            "peer", "lifecycle", "chaincode", "approveformyorg",
            "--channelID", channel_name,
            "--name", chaincode_name,
            "--version", chaincode_version,
            "--package-id", package_id,
            "--sequence", "1",
            "--tls", 
            "--cafile", "/etc/hyperledger/fabric/orderercert/tls/ca.crt",
            "--orderer", "orderer1.example.com:7050",
            "--signature-policy", endorsement_policy
        ]

        result = subprocess.run(command, capture_output=True, text=True)
            

        if result.returncode == 0:
            print(f"Chaincode approved successfully on {peer_address}.")
        else:
            print(f"Error approving chaincode on {peer_address}: {result.stderr}")



def commit():
    # 커밋 명령 구성
    cli_container_name = "hyperledger/fabric-tools:2.5.6"
    # ordererCaCert="../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt"
    peer_address="peer0.org1.example.com:7051"
    # tls_root_cert_file="../organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
    #   -e CORE_PEER_TLS_ROOTCERT_FILE=/fabric/config/peers/peer0.org1.example.com/tls/ca.crt \

    command = [
        "docker", "run", 
        "--rm",
        "--network", "fabric_test",
        "-v", "/home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/organizations:/organizations",
        cli_container_name,
        "env",
        "CORE_PEER_MSPCONFIGPATH=/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp",
        "CORE_PEER_TLS_ENABLED=true",
        "CORE_PEER_TLS_ROOTCERT_FILE=/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt",
        "CORE_PEER_LOCALMSPID=Org1MSP",
        "peer", "lifecycle", "chaincode", "commit",
        "--channelID", channel_name,
        "--name", chaincode_name,
        "--version", chaincode_version,
        "--sequence", "1",
        "--tls", 
        "--cafile", "/organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt",
        "--orderer", "orderer1.example.com:7050",
        "--peerAddresses", "peer0.org1.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org2.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org3.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org4.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org4.example.com/peers/peer0.org4.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org5.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org5.example.com/peers/peer0.org5.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org6.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org6.example.com/peers/peer0.org6.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org7.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org7.example.com/peers/peer0.org7.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org8.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org8.example.com/peers/peer0.org8.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org9.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org9.example.com/peers/peer0.org9.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org10.example.com:7051",
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org10.example.com/peers/peer0.org10.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org11.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org11.example.com/peers/peer0.org11.example.com/tls/ca.crt",
        "--peerAddresses", "peer0.org12.example.com:7051", 
        "--tlsRootCertFiles", "/organizations/peerOrganizations/org12.example.com/peers/peer0.org12.example.com/tls/ca.crt",
        "--signature-policy", endorsement_policy
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Chaincode committed successfully.")
    else:
        print(f"Error committing chaincode: {result.stderr}")

# 1. create channel (?) 할 필요 없음 in v2.5.6
# 2. join channel 각자.
# 3. install chain code 각자
# 4. approve 각자
# 5. commit chain code definition 한번
actions = {
    'create': createchannel,
    'join': join_peers,
    'install': install_cc,
    'approve': approve,
    'commit': commit,
}

# 실행
if args.action in actions:
    actions[args.action]()
else:
    print("Invalid action")