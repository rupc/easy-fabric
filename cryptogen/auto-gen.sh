#!/bin/bash
BINPATH="../bins/bin-v2.5.6/"

$BINPATH/cryptogen generate --config=./organizations-6-zones/crypto-config-6-orderer.yaml --output="organizations-6-zones"
$BINPATH/cryptogen generate --config=./organizations-6-zones/crypto-config-24-org.yaml --output="organizations-6-zones"

$BINPATH/cryptogen generate --config=./organizations-9-zones/crypto-config-9-orderer.yaml --output="organizations-9-zones"
$BINPATH/cryptogen generate --config=./organizations-9-zones/crypto-config-36-org.yaml --output="organizations-9-zones"

$BINPATH/cryptogen generate --config=./organizations-12-zones/crypto-config-12-orderer.yaml --output="organizations-12-zones"
$BINPATH/cryptogen generate --config=./organizations-12-zones/crypto-config-48-org.yaml --output="organizations-12-zones"

$BINPATH/cryptogen generate --config=./organizations-15-zones/crypto-config-15-orderer.yaml --output="organizations-15-zones"
$BINPATH/cryptogen generate --config=./organizations-15-zones/crypto-config-60-org.yaml --output="organizations-15-zones"

# $BINPATH/cryptogen generate --config=./organizations-3-zones/crypto-config-3-orderer.yaml --output="organizations-3-zones"
# $BINPATH/cryptogen generate --config=./organizations-3-zones/crypto-config-24-org.yaml --output="organizations-3-zones"
