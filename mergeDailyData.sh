#! /usr/bin/bash
cd /home/ospe/repos/tennis-data/
TARGET_DIR="./data/merged_files"

if [ ! -d "$TARGET_DIR" ]; then
	mkdir -p "$TARGET_DIR"

fi

cat ./data/$1/*.json | jq -s '.' > ./$TARGET_DIR/$1.json
