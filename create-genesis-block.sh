#!/bin/bash

# Set the path to the configtxgen binary
BINPATH="bins/bin-v2.5.6/"

# Check if the channel-artifacts directory exists, if not create it
if [ ! -d "./channel-artifacts" ]; then
    mkdir ./channel-artifacts
    echo "Created directory: ./channel-artifacts"
fi

organizations=(
    "12orgs-3orderers"
    "24orgs-6orderers"
    "36orgs-9orderers"
    "48orgs-12orderers"
    "60orgs-15orderers"
)

for org_path in "${organizations[@]}"; do
    echo "Processing $org_path..."
    rm -rf ./organizations
    cp cryptogen/organizations-$org_path ./organizations -rf

    CONFIGPATH="./configtx/configtx-${org_path}"

    $BINPATH/configtxgen -profile ChannelUsingRaft -configPath "$CONFIGPATH" -outputBlock "./channel-artifacts/${org_path}.genesis.block" -channelID mychannel
done
