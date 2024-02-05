#! /usr/bin/bash

cd /home/ospe/repos/tennis-data/
CURRENT_DATE=$(date +"%Y-%m-%d")
TARGET_FILE="./data/$CURRENT_DATE"

if [ ! -d "$TARGET_FILE" ]; then
    mkdir -p "$TARGET_FILE"
fi

source ./venv/bin/activate
python ./tennisScraper.py
deactivate
