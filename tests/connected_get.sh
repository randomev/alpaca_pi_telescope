#!/bin/bash

source config.sh

# Test Connected API
echo "Testing Connected API..."
curl "$ALPACA_SERVER/api/v1/telescope/0/connected?$BP"
