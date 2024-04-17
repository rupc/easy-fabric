#!/bin/bash

# Set the path to the configtxgen binary
BINPATH="bins/bin-v2.5.6/"

# Check if the channel-artifacts directory exists, if not create it
if [ ! -d "./channel-artifacts" ]; then
    mkdir ./channel-artifacts
    echo "Created directory: ./channel-artifacts"
fi

organizations=(
    "cryptogen/organizations-24org-6orderer"
    "cryptogen/organizations-36org-9orderer"
    "cryptogen/organizations-48org-12orderer"
    "cryptogen/organizations-60org-15orderer"
)

for org_path in "${organizations[@]}"; do
    echo "Processing $org_path..."
    # 여기에 각 경로에 대해 실행할 명령을 삽입합니다.
    # 예: config 파일 생성 또는 파일 복사 등
done

# Loop through all yaml files in the configtx directory
for CONFIGPATH in ./configtx/configtx-*; do

    # Extract the filename without path and extension
    BASENAME=$(basename -- "$CONFIGPATH")
    FILENAME="${BASENAME%.*}"

    # Generate the genesis block using configtxgen
    echo "Processing $CONFIGPATH..."
    $BINPATH/configtxgen -profile ChannelUsingRaft -configPath "$CONFIGPATH" -outputBlock "./channel-artifacts/${FILENAME}.genesis.block" -channelID mychannel

    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Genesis block generated for $FILENAME"
    else
        echo "Failed to generate genesis block for $FILENAME"
    fi
done
