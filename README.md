# BugMoe Backup

BugMoe Minecraft Map 備份工具

## 系統需求

### Windows
- Windows 10 或更新版本
- 不需要安裝其他軟體

### macOS
- macOS 10.15 或更新版本

## 使用方法

### Windows 使用者
1. 直接執行方式：
   ```
   BugMoeBackup.exe [來源資料夾] [目標資料夾]
   ```

2. 使用批次檔（推薦）：
   - 雙擊執行 `BugMoeBackup.bat`
   - 依照提示輸入來源和目標資料夾
   - 等待備份完成

### macOS 直接執行
```bash
./dist/backup_bugmoe <source_folder> <destination_folder>
```

或者：
```bash
./dist/BugMoeBackup <source_folder> <destination_folder>
```

### 開發者：使用 Docker
1. 安裝 Docker Desktop
2. 在專案目錄中執行：
```bash
./docker-run.sh <source_folder> <destination_folder>
```

## 參數說明

- `source_folder`: Minecraft 地圖來源資料夾路徑
- `destination_folder`: 備份目標資料夾路徑

## 注意事項

1. Windows 使用者建議使用 `BugMoeBackup.bat`，它提供更友善的使用介面
2. 備份過程中請勿關閉程式
3. 建議定期進行備份測試，確保備份的完整性

## 開發者說明

### 編譯 Windows 執行檔
```bash
./build_windows.sh
```
編譯完成後的執行檔位於 `dist/BugMoeBackup.exe`
