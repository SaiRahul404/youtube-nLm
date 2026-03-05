@echo off
echo.
echo =========================================
echo  Remove YouTube NotebookLM Automation
echo =========================================
echo.
echo This will remove the scheduled task.
echo.
pause

:: Run PowerShell script as Administrator
powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0remove_scheduler.ps1\"' -Verb RunAs"
