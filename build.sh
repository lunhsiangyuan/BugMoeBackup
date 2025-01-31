#!/bin/bash

# 確保腳本在錯誤時停止
set -e

echo "開始建立 BugMoe 備份工具..."

# 建立 Docker 映像
echo "步驟 1/4: 建立 Docker 映像..."
docker build -t bugmoe-builder .

# 建立輸出目錄
echo "步驟 2/4: 準備輸出目錄..."
mkdir -p ./dist

# 執行容器並複製檔案
echo "步驟 3/4: 執行編譯..."
docker run --name bugmoe-build bugmoe-builder
docker cp bugmoe-build:/dist/. ./dist/
docker rm bugmoe-build

echo "步驟 4/4: 清理暫存檔..."
docker rmi bugmoe-builder

echo "完成！"
echo "編譯好的檔案在 ./dist 目錄中"
ls -l ./dist 