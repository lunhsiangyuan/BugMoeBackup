# 第一階段：安裝依賴和編譯
FROM --platform=linux/amd64 ubuntu:20.04 as builder

WORKDIR /app

# 安裝必要的套件
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wine64 \
    wget \
    unzip \
    xvfb

# 下載並安裝 Python embedded 版本
RUN wget https://www.python.org/ftp/python/3.11.0/python-3.11.0-embed-amd64.zip && \
    mkdir -p /opt/python-win && \
    unzip python-3.11.0-embed-amd64.zip -d /opt/python-win && \
    rm python-3.11.0-embed-amd64.zip && \
    wget https://bootstrap.pypa.io/get-pip.py -O /opt/python-win/get-pip.py && \
    wine64 /opt/python-win/python.exe /opt/python-win/get-pip.py

# 設定 Python 環境變數
ENV WINEPATH="/opt/python-win;/opt/python-win/Scripts"

# 複製源碼
COPY . .

# 使用 wine64 安裝相依套件
RUN wine64 /opt/python-win/python.exe -m pip install --no-cache-dir pyinstaller && \
    wine64 /opt/python-win/python.exe -m pip install -r requirements.txt

# 使用 PyInstaller 打包
RUN wine64 /opt/python-win/python.exe -m PyInstaller --onefile backup_bugmoe.py

# 第二階段：準備發布檔案
FROM --platform=linux/amd64 alpine:latest

WORKDIR /dist

# 從第一階段複製編譯好的檔案
COPY --from=builder /app/dist/backup_bugmoe.exe .
COPY --from=builder /app/run_backup.bat .
COPY --from=builder /app/README.md .

# 設定輸出目錄
VOLUME /dist

# 保持容器運行
CMD ["cp", "/dist/backup_bugmoe.exe", "/output/"]
