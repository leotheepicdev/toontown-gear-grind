#!/bin/sh
cd ../..

# Define some constants for our AI server:
MAX_CHANNELS=999999
STATESERVER=4002
ASTRON_IP="127.0.0.1:7101"
EVENTLOGGER_IP="127.0.0.1:7197"

# Get the user input:
read -p "District name (DEFAULT: Sillyville): " DISTRICT_NAME
DISTRICT_NAME=${DISTRICT_NAME:-Sillyville}
read -p "Base channel (DEFAULT: 401000000): " BASE_CHANNEL
BASE_CHANNEL=${BASE_CHANNEL:-401000000}

export WANT_RANDOM_INVASIONS=1
export WANT_INVASIONS_ONLY=0

while [ true ]
do
    python3 -m toontown.ai.AIStart --base-channel $BASE_CHANNEL \
                     --max-channels $MAX_CHANNELS --stateserver $STATESERVER \
                     --astron-ip $ASTRON_IP --eventlogger-ip $EVENTLOGGER_IP --want-random-invasions $WANT_RANDOM_INVASIONS --want-invasions-only $WANT_INVASIONS_ONLY  \
                     --district-name "$DISTRICT_NAME"
done
