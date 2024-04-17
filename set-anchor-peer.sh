#!/bin/bash

# 기본 설정
ANCHOR_PEER_PORT=7051
CHANNEL_NAME="mychannel"
BIN_PATH="./bins/bin-v2.5.6"
# config.json 파일이 있는 경로를 지정하세요.
CONFIG_JSON_PATH="./config.json"

function create_anchor_peer_update() {
    cp $CONFIG_JSON_PATH temp_config.json

    for ORG_NUM in {2..12}; do
        # 각 조직에 대한 설정
        MSP_ID="Org${ORG_NUM}MSP"
        ANCHOR_PEER_HOST="peer0.org${ORG_NUM}.example.com"

        CORE_PEER_TLS_ENABLED=true CORE_PEER_MSPCONFIGPATH=../../organizations/peerOrganizations/org$ORG_NUM.example.com/users/Admin@org$ORG_NUM.example.com/msp FABRIC_CFG_PATH=./deployment/config CORE_PEER_LOCALMSPID=$MSP_ID CORE_PEER_TLS_ROOTCERT_FILE=../../organizations/peerOrganizations/org$ORG_NUM.example.com/peers/peer0.org$ORG_NUM.example.com/tls/ca.crt ${BIN_PATH}/peer channel fetch config config_block.pb -o localhost:7060 -c mychannel --tls --cafile ../../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt
        echo "Fetched config block for ${MSP_ID}"

        bins/bin-v2.5.6/configtxlator proto_decode --input config_block.pb --type common.Block | jq '.data.data[0].payload.data.config' >config.json
        echo "created latest config.json"

        # jq 명령어 실행
        jq --arg MSP_ID "$MSP_ID" \
            --arg ANCHOR_PEER_HOST "$ANCHOR_PEER_HOST" \
            --argjson ANCHOR_PEER_PORT $ANCHOR_PEER_PORT \
            '.channel_group.groups.Application.groups[$MSP_ID].values += {"AnchorPeers":{"mod_policy": "Admins","value":{"anchor_peers": [{"host": $ANCHOR_PEER_HOST,"port": $ANCHOR_PEER_PORT}]},"version": "0"}}' \
            $CONFIG_JSON_PATH >"modified_config_$ORG_NUM.json"

        # 결과 확인
        echo "Modified config for ${MSP_ID} written to modified_config_${ORG_NUM}.json"

        # config.json modified_config.json anchors.tx
        original="config.json"
        modified="modified_config_$ORG_NUM.json"

        echo "Computing config update for ${MSP_ID}"
        ${BIN_PATH}/configtxlator proto_encode --input "${original}" --type common.Config --output original_config.pb
        ${BIN_PATH}/configtxlator proto_encode --input "${modified}" --type common.Config --output modified_config_"$ORG_NUM".pb

        # returns non-zero if no updates were detected between current and new config
        ${BIN_PATH}/configtxlator compute_update --channel_id "${CHANNEL_NAME}" --original original_config.pb --updated modified_config_"$ORG_NUM".pb --output config_update.pb
        if [ $? -ne 0 ]; then
            echo "Anchor peer has already been set to ${ANCHOR_PEER_HOST}:${ANCHOR_PEER_PORT} - no update required."
            return 1
        fi

        echo "Decoding config update to JSON and isolating config to config_update.json"
        ${BIN_PATH}/configtxlator proto_decode --input config_update.pb --type common.ConfigUpdate --output config_update.json

        echo "Creating envelope for config update and writing to anchors.tx"
        output="anchors.tx"
        echo '{"payload":{"header":{"channel_header":{"channel_id":"'${CHANNEL_NAME}'", "type":2}},"data":{"config_update":'$(cat config_update.json)'}}}' | jq . >config_update_in_envelope.json
        ${BIN_PATH}/configtxlator proto_encode --input config_update_in_envelope.json --type common.Envelope --output ${output}

        echo "submitting anchortx for ${MSP_ID} "
        FABRIC_CFG_PATH=./deployment/config CORE_PEER_MSPCONFIGPATH=../../organizations/peerOrganizations/org$ORG_NUM.example.com/users/Admin@org$ORG_NUM.example.com/msp CORE_PEER_TLS_ROOTCERT_FILE=../../organizations/peerOrganizations/org$ORG_NUM.example.com/peers/peer0.org$ORG_NUM.example.com/tls/ca.crt CORE_PEER_LOCALMSPID=${MSP_ID} CORE_PEER_TLS_ENABLED=true ${BIN_PATH}/peer channel \
            update -f anchors.tx \
            -o localhost:7060 \
            -c ${CHANNEL_NAME} \
            --tls --cafile ../../organizations/ordererOrganizations/example.com/orderers/orderer1.example.com/tls/ca.crt

        echo "sleep 5 for MSP ${MSP_ID}"
        sleep 5
    done

}

function create_config_update() {
    local original=$1
    local modified=$2
    local output=$3

}

create_anchor_peer_update
