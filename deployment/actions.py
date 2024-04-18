#!/usr/bin/python3
import subprocess
import yaml
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# argparse를 사용하여 커맨드 라인 인자 처리
parser = argparse.ArgumentParser(
    description='Manage chaincode on Fabric network.')
parser.add_argument('action', type=str, choices=['join', 'install', 'instan', 'approve',
                    'commit', 'anchor_fetch', 'anchor'], help='Action to perform: join, install, or instan')
args = parser.parse_args()

# Read the bench-config.yaml
with open('bench-config.yaml', 'r') as file:
    config = yaml.safe_load(file)


bin_path = "../../bin"

# 채널 구성 블록 파일의 경로

# CLI 컨테이너 이름
cli_container_name = "peer0.org1.example.com"
network_name = "fabric_test"  # Local test
# network_name = "hlfcaliper" # Distributed test

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

print("bench_config", config)

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


def join_peer(i):
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
        print(
            f"Failed to join peer {peer_address} to {channel_name}. Error: {result.stderr}")


def join_peers():
    with ThreadPoolExecutor(max_workers=peer_count) as executor:
        executor.map(join_peer, range(peer_count))


# def package():
chaincode_name = "smallbank"
chaincode_version = "v1.0"


def install_chaincode_on_peer(i):
    peer_address = f"peer{0}.org{i+1}.example.com:7051"
    tls_root_cert_file = "/etc/hyperledger/fabric/tls/ca.crt"
    package_file = f"{chaincode_name}_{chaincode_version}.tar.gz"
    package_path = "/etc/hyperledger/fabric/chaincode/"
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


def install_cc():
    with ThreadPoolExecutor(max_workers=peer_count) as executor:
        executor.map(install_chaincode_on_peer, range(peer_count))

# peer lifecycle chaincode commit -o orderer.example.com:7050 --channelID mychannel --name smallbank --version 1.0 --sequence 1 --tls true --cafile $ORDERER_CA --signature-policy "AND('Org1MSP.peer','Org2MSP.peer','Org3MSP.peer','Org4MSP.peer')"


def instantiate_cc():
    print("Instantiating chaincode...")
    pass

# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode approveformyorg --channelID mychannel --name smallbank --version 1.0 --sequence 1 --package-id smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050
# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode commit  --channelID mychannel --name smallbank --version 1.0 --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050 --signature-policy "OR('Org1MSP.peer')"
# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode commit  --channelID mychannel --name smallbank --version 1.0 --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050


# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode approveformyorg --channelID mychannel --name smallbank --version 1.0 --package-id smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13 --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt --orderer orderer1.example.com:7050 --signature-policy "AND('Org1MSP.peer', 'Org2MSP.peer', 'Org3MSP.peer', 'Org4MSP.peer', 'Org5MSP.peer', 'Org6MSP.peer', 'Org7MSP.peer', 'Org8MSP.peer', 'Org9MSP.peer', 'Org10MSP.peer', 'Org11MSP.peer', 'Org12MSP.peer')"


# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode queryapproved --channelID mychannel --name smallbank --sequence 1 --tls --cafile /etc/hyperledger/fabric/orderercert/tls/ca.crt
# CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/adminmsp peer lifecycle chaincode queryinstalled

# peer lifecycle chaincode approveformyorg -o orderer.example.com:7050 --channelID mychannel --name mycc --version 1.0 --sequence 1 --tls true --cafile /path/to/orderer/ca --signature-policy

# 체인코드 커밋 (이 명령은 채널의 모든 조직에 대해 실행해야 할 수도 있습니다)
# peer lifecycle chaincode commit -o orderer.example.com:7050 --channelID mychannel --name mycc --version 1.0 --sequence 1 --tls true --cafile /path/to/orderer/ca --peerAddresses peer0.org1.example.com:7051 --tlsRootCertFiles /path/to/org1/peer0/tls/ca.crt --signature-policy "OR('Org1MSP.member', 'Org2MSP.member', 'Org3MSP.member', 'Org4MSP.member', 'Org5MSP.member', 'Org6MSP.member', 'Org7MSP.member', 'Org8MSP.member', 'Org9MSP.member', 'Org10MSP.member', 'Org11MSP.member', 'Org12MSP.member')"
cli_container_name = "hyperledger/fabric-tools:2.5.6"


def GetEndorsementPolicy(num_org, option):
    endorsement_policy = ""
    if option == "single":
        endorsement_policy = "OR(" + ", ".join(
            ['\'Org'+str(i+1)+'MSP.member\'' for i in range(num_org)]) + ")"
    elif option == "outof":
        n = int((num_org / 2) + 1)
        # 'OutOf' 함수를 사용해 지정된 수의 조건을 충족하는 규칙을 만듭니다.
        # 이때, out_of 값과 조직 멤버 조건들을 올바르게 포맷팅하여 문자열로 구성합니다.
        endorsement_policy = "OutOf(" + str(n) + "," + ",".join(
            ['\'Org'+str(i+1)+'MSP.member\'' for i in range(num_org)]) + ")"
    else:
        endorsement_policy = ""

    return str(endorsement_policy)


# endorsement_policy = "OutOf(4, 'Org1MSP.peer', 'Org2MSP.peer', 'Org3MSP.peer', 'Org4MSP.peer', 'Org5MSP.peer', 'Org6MSP.peer', 'Org7MSP.peer', 'Org8MSP.peer', 'Org9MSP.peer', 'Org10MSP.peer', 'Org11MSP.peer', 'Org12MSP.peer')"
# single_endorsement_policy = "OR('Org1MSP.member', 'Org2MSP.member', 'Org3MSP.member', 'Org4MSP.member', 'Org5MSP.member', 'Org6MSP.member', 'Org7MSP.member', 'Org8MSP.member', 'Org9MSP.member', 'Org10MSP.member', 'Org11MSP.member', 'Org12MSP.member')"


sequence = "1"
package_id = "smallbank_v1.0:54fdc719a38bea2264e254342e9a47be265d0a761c55b3ebbe1ec690fc8efd13"  # 승인할 체인코드 패키지 ID


def approve_chaincode_on_peer(i):
    peer_address = f"peer0.org{i+1}.example.com:7051"
    peer_address_without_port = peer_address.split(":")[0]
    tls_root_cert_file = f"/etc/hyperledger/fabric/tls/ca.crt"
    endorsement_policy = GetEndorsementPolicy(peer_count, "single")
    command = [
        "docker", "run",
        "--rm",
        "--network", "fabric_test",
        "-v", "/home/jyr/go/src/github.com/rupc/fabric-benchmarks/fabric-samples/bench-network/organizations:/organizations",
        cli_container_name,
        "env",
        f"CORE_PEER_TLS_ENABLED=true",
        f"CORE_PEER_ADDRESS={peer_address}",
        f"CORE_PEER_TLS_ROOTCERT_FILE=/organizations/peerOrganizations/org{i+1}.example.com/peers/{peer_address_without_port}/tls/ca.crt",
        f"CORE_PEER_LOCALMSPID=Org{i+1}MSP",
        f"CORE_PEER_MSPCONFIGPATH=/organizations/peerOrganizations/org{i+1}.example.com/users/Admin@org{i+1}.example.com/msp",
        "peer", "lifecycle", "chaincode", "approveformyorg",
        "--channelID", channel_name,
        "--name", chaincode_name,
        "--version", chaincode_version,
        "--package-id", package_id,
        "--sequence", sequence,
        "--tls",
        "--cafile", "/organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt",
        "--orderer", "orderer1.example.com:7050",
        "--signature-policy", endorsement_policy
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Chaincode approved successfully on {peer_address}.")
    else:
        print(f"Error approving chaincode on {peer_address}: {result.stderr}")


def approve():
    # print(GetEndorsementPolicy(peer_count, "single"))

    with ThreadPoolExecutor(max_workers=peer_count) as executor:
        executor.map(approve_chaincode_on_peer, range(peer_count))


def generate_flags(num_peers):
    flags = []
    for i in range(1, num_peers + 1):
        peer_address = f"peer0.org{i}.example.com:7051"
        tls_root_cert_file = f"/organizations/peerOrganizations/org{i}.example.com/peers/peer0.org{i}.example.com/tls/ca.crt"

        flags.extend([
            "--peerAddresses", peer_address,
            "--tlsRootCertFiles", tls_root_cert_file
        ])
    return flags


def commit():
    # 커밋 명령 구성
    cli_container_name = "hyperledger/fabric-tools:2.5.6"
    endorsement_policy = GetEndorsementPolicy(peer_count, "single")

    # ordererCaCert="../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt"
    peer_address = "peer0.org1.example.com:7051"
    # tls_root_cert_file="../organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
    #   -e CORE_PEER_TLS_ROOTCERT_FILE=/fabric/config/peers/peer0.org1.example.com/tls/ca.crt \
    commitFlags = generate_flags(peer_count)

    command = [
        "docker", "run",
        "--rm",
        "--network", network_name,
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
        "--sequence", sequence,
        "--tls",
        "--cafile", "/organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt",
        "--orderer", "orderer1.example.com:7050",
        *commitFlags,
        "--signature-policy", endorsement_policy
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Chaincode committed successfully.")
    else:
        print(f"Error committing chaincode: {result.stderr}")


def set_anchor_peer(org_index):

    anchor_peer_tx = f"Org{org_index}MSPanchors.tx"
    configtxgen_cmd = [
        "export CORE_PEER_LOCALMSPID "
        "configtxgen",
        "-profile", "YourChannelProfile",
        "-outputAnchorPeersUpdate", anchor_peer_tx,
        "-channelID", CHANNEL_NAME,
        "-asOrg", f"Org{org_index}MSP"
    ]
    subprocess.run(configtxgen_cmd, check=True)

    peer_cmd = [
        "peer", "channel", "update",
        "-f", anchor_peer_tx,
        "-c", CHANNEL_NAME,
        "-o", ORDERER_ADDRESS,
        "--tls", "--cafile", ORDERER_CERT
    ]
    # MSP 설정이 필요할 수 있습니다. 예: CORE_PEER_LOCALMSPID 및 CORE_PEER_MSPCONFIGPATH
    subprocess.run(peer_cmd, check=True)


def anchor_fetch():
    cli_container_name = "hyperledger/fabric-tools:2.5.6"
    # ordererCaCert="../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt"
    # peer_address="peer0.org1.example.com:7051"
    # tls_root_cert_file="../organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
    #   -e CORE_PEER_TLS_ROOTCERT_FILE=/fabric/config/peers/peer0.org1.example.com/tls/ca.crt \
# peer channel fetch config config_block.pb -o [ORDERER_ADDRESS] -c [CHANNEL_NAME] --tls --cafile [ORDERER_CA]

    # channel fetch config config_block.pb -o 0.0.0.0:7050 -c mychannel --tls --cafile ../../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt
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
        "peer", "channel", "fetch", "config", "config_block.pb",
        "-o", "orderer1.example.com:7050",
        "-c", channel_name,
        "--tls",
        "--cafile", "/organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Anchor fetch successfully.")
    else:
        print(f"Error Anchor fetch chaincode: {result.stderr}")


def update_anchor():
    NUM_ORGS = 12
    for org_index in range(1, NUM_ORGS + 1):
        set_anchor_peer(org_index)


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
    'anchor_fetch': anchor_fetch,
    'anchor': update_anchor,
}

# 실행
if args.action in actions:
    actions[args.action]()
else:
    print("Invalid action")
