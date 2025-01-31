# BugMoe Backup

BugMoe Minecraft Map 備份工具

## 系統需求

- Windows 10 或更新版本
- 不需要安裝其他軟體

## 使用方法

直接執行方式：
```
BugMoeBackup.exe [來源資料夾] [目標資料夾]
```

## 參數說明

- `source_folder`: Minecraft 地圖來源資料夾路徑
- `destination_folder`: 備份目標資料夾路徑

## 注意事項

1. 備份過程中請勿關閉程式
2. 建議定期進行備份測試，確保備份的完整性

## 開發者說明

本專案使用 GitHub Actions 自動編譯 Windows 執行檔。當有新的提交時，會自動觸發編譯流程，您可以在 Actions 頁面下載最新的執行檔。
