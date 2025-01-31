@echo off
echo BugMoe Minecraft 地圖備份工具
echo ===========================
echo.

if "%~1"=="" goto usage
if "%~2"=="" goto usage

BugMoeBackup.exe "%~1" "%~2"
goto end

:usage
echo 使用方法：
echo BugMoeBackup.bat [來源資料夾] [目標資料夾]
echo.
echo 範例：
echo BugMoeBackup.bat "C:\Minecraft\saves\MyWorld" "D:\Backup"
echo.
pause

:end 