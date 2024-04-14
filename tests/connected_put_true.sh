#!/bin/bash

source config.sh

# Test Connected API
echo "Connected PUT = true"
curl -X PUT \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "Connected=true" \
     -d "ClientID=1" \
     -d "ClientTransactionId=1" \
     "$ALPACA_SERVER/api/v1/telescope/0/connected"

echo "Checking with GET"

./connected_get.sh