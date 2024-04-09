#!/bin/bash

../bin/cryptogen generate --config=./cryptogen/crypto-config-orderer.yaml
../bin/cryptogen generate --config=./cryptogen/crypto-config-12-org.yaml
mkdir organizations
mv crypto-config/* organizations
