#!/bin/bash

source config.sh

# Test Pulseguide API
echo "Pulseguide PUT"
curl -X PUT \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "Duration=2000" \
     -d "Direction=1" \
     -d "ClientID=1" \
     -d "ClientTransactionId=1" \
     "$ALPACA_SERVER/api/v1/telescope/0/pulseguide"

sleep 0.5
echo "Checking with Slewing GET should return true"
./slewing_get.sh
sleep 2.0
echo "Checking with Slewing GET should return false"
./slewing_get.sh
