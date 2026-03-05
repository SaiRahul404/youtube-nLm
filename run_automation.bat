@echo off
REM YouTube NotebookLM Automation - Windows Task Scheduler Wrapper

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the Python script
python src\main.py

REM Deactivate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\deactivate.bat
)

REM Exit with the Python script's exit code
exit /b %ERRORLEVEL%
