#!/bin/bash

# 檢查參數
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <source_folder> <destination_folder>"
    exit 1
fi

SOURCE_FOLDER="$1"
DEST_FOLDER="$2"

# 建立 Docker 映像
docker build -t bugmoe-backup .

# 運行容器
docker run --rm -v "$SOURCE_FOLDER":/source -v "$DEST_FOLDER":/destination \
    bugmoe-backup /source /destination 