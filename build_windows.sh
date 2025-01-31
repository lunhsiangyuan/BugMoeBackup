#!/bin/bash

echo "開始編譯 Windows 執行檔..."

# 確保使用 x86_64 架構
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# 建立輸出目錄
mkdir -p output

# 建立 Docker 映像並執行
echo "建立 Docker 映像並編譯..."
docker build -t bugmoe-backup-builder -f Dockerfile.build .
docker run --rm -v "$(pwd)/output:/output" bugmoe-backup-builder

# 移動執行檔到 dist 目錄
echo "移動執行檔..."
mv output/BugMoeBackup.exe dist/

# 清理
echo "清理暫存檔..."
rm -rf output
docker rmi bugmoe-backup-builder

echo "編譯完成！執行檔位於 dist/BugMoeBackup.exe"
echo "您可以：
1. 將檔案複製到 Parallels Windows 中測試
2. 確認無誤後再給小朋友使用" 