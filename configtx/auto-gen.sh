#!/bin/bash

./configtxgen.py --num_orgs 12 --num_orderers 3
./configtxgen.py --num_orgs 24 --num_orderers 6
./configtxgen.py --num_orgs 36 --num_orderers 9
./configtxgen.py --num_orgs 48 --num_orderers 12
./configtxgen.py --num_orgs 60 --num_orderers 15
