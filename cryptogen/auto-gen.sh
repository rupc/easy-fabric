#!/bin/bash
BINPATH="../bins/bin-v2.5.6/"

# profiles=(
#     "12orgs-3orderers",
#     "24orgs-6orderers",
#     "36orgs-9orderers",
#     "48orgs-12orderers",
#     "60orgs-12orderers",
# )
# for profile in "${profiles[@]}"; do
#     echo "Processing $profile..."

#     mkdir -p organizations-${profile}

#     $BINPATH/cryptogen generate --config=./$profile/crypto-config-3-orderer.yaml --output="$profile"
#     $BINPATH/cryptogen generate --config=./$profile/crypto-config-24-org.yaml --output="$profile"
# done

# ./generate 12orgs-3orderers
$BINPATH/cryptogen generate --config=./organizations-12orgs-3orderers/crypto-config-3-orderer.yaml --output="organizations-12orgs-3orderers"
$BINPATH/cryptogen generate --config=./organizations-12orgs-3orderers/crypto-config-24-org.yaml --output="organizations-12orgs-3orderers"

# $BINPATH/cryptogen generate --config=./organizations-24orgs-6orderers/crypto-config-6-orderer.yaml --output="organizations-24orgs-6orderers"
# $BINPATH/cryptogen generate --config=./organizations-24orgs-6orderers/crypto-config-24-org.yaml --output="organizations-24orgs-6orderers"

$BINPATH/cryptogen generate --config=./organizations-36orgs-9orderers/crypto-config-9-orderer.yaml --output="organizations-36orgs-9orderers"
$BINPATH/cryptogen generate --config=./organizations-36orgs-9orderers/crypto-config-36-org.yaml --output="organizations-36orgs-9orderers"

$BINPATH/cryptogen generate --config=./organizations-48orgs-12orderers/crypto-config-12-orderer.yaml --output="organizations-48orgs-12orderers"
$BINPATH/cryptogen generate --config=./organizations-48orgs-12orderers/crypto-config-48-org.yaml --output="organizations-48orgs-12orderers"

$BINPATH/cryptogen generate --config=./organizations-60orgs-15orderers/crypto-config-15-orderer.yaml --output="organizations-60orgs-15orderers"
$BINPATH/cryptogen generate --config=./organizations-60orgs-15orderers/crypto-config-60-org.yaml --output="organizations-60orgs-15orderers"
