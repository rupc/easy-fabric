#! /bin/bash

BIN_PATH="../bin"

function GenerateGenesisBlock() {
    # 2. Generate genesis block (for ordering service)
    ${BIN_PATH}/configtxgen -profile ChannelUsingRaft -configPath ./bftconfigtx -outputBlock ./channel-artifacts/genesis.block -channelID mychannel
}

function Credential() {
    # 1. Generate credentials for all participating nodes (public/private keys, certificates, etc.)
    ${BIN_PATH}/cryptogen generate --config=./cryptogen/crypto-config-org1.yaml
    ${BIN_PATH}/cryptogen generate --config=./cryptogen/crypto-config-orderer.yaml
}

# 4. OSN Admin 사용해서, 채널 생성 (오더러를 채널에 조인)
# function OSNCreateChannel() {

#     export OSN_TLS_CA_ROOT_CERT=/var/hyperledger/orderer/tls/ca.crt
#     export ADMIN_TLS_SIGN_CERT=/var/hyperledger/orderer/adminmsp/signcerts/Admin@example.com-cert.pem
#     export ADMIN_TLS_PRIVATE_KEY=/var/hyperledger/orderer/adminmsp/keystore/priv_sk

#     ordererAddr="localhost:7060"
#     ${BIN_PATH}/osnadmin channel join --channelID mychannel --config-block ./channel-artifacts/genesis.block -o ${ordererAddr} --ca-file $OSN_TLS_CA_ROOT_CERT --client-cert $ADMIN_TLS_SIGN_CERT --client-key $ADMIN_TLS_PRIVATE_KEY

#     # bin/osnadmin channel join --channelID mychannel --config-block ./channel-artifacts/genesis.block -o localhost:7060 --ca-file organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt --client-cert
#     # bin/osnadmin channel join --channelID mychannel --config-block ./orderer/orderer.genesis.block -o orderer1.example.com:7053 --ca-file /var/hyperledger/orderer/tlsca/tlsca.example.com-cert.pem --client-cert /var/hyperledger/orderer/tls/server.crt --client-key /var/hyperledger/orderer/tls/server.key
#     bin/osnadmin channel join --channelID mychannel --config-block ./orderer/orderer.genesis.block -o orderer1.example.com:7053 --ca-file /var/hyperledger/orderer/tlsca/tlsca.example.com-cert.pem --client-cert /var/hyperledger/orderer/adminmsp/signcerts/Admin@example.com-cert.pem --client-key /var/hyperledger/orderer/adminmsp/keystore/priv_sk
#     # bin/osnadmin channel join --channelID mychannel --config-block ./orderer/orderer.genesis.block -o orderer1.example.com:7053 --ca-file /var/hyperledger/orderer/tlsca/tlsca.example.com-cert.pem --client-cert /var/hyperledger/orderer/adminmsp/signcerts/Admin@example.com-cert.pem --client-key /var/hyperledger/orderer/adminmsp/keystore/priv_sk

#     ORDERER_CA=${DIR}/test-network/organizations/ordererOrganizations/example.com/tlsca/tlsca.example.com-cert.pem

#     export PATH=${ROOTDIR}/../bin:${PWD}/../bin:$PATH
#     export ORDERER_ADMIN_TLS_SIGN_CERT=${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.crt /dev/null 2>&1
#     export ORDERER_ADMIN_TLS_PRIVATE_KEY=${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.key /dev/null 2>&1

#     osnadmin channel join --channelID ${channel_name} --config-block ./channel-artifacts/${channel_name}.block -o localhost:7053 --ca-file "$ORDERER_CA" --client-cert "$ORDERER_ADMIN_TLS_SIGN_CERT" --client-key "$ORDERER_ADMIN_TLS_PRIVATE_KEY" >>log.txt 2>&1
# }

OSNCreateChannel
