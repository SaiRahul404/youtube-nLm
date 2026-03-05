@echo off
echo.
echo =========================================
echo  YouTube NotebookLM Task Scheduler Setup
echo =========================================
echo.
echo This will set up automatic execution every 12 hours.
echo.
pause

:: Run PowerShell script as Administrator
powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0setup_scheduler.ps1\"' -Verb RunAs"
