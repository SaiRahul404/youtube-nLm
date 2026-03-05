@echo off
REM Quick Setup Script for YouTube NotebookLM Automation POC

echo ====================================
echo YouTube NotebookLM Automation Setup
echo ====================================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Step 1: Creating Python virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create virtual environment
    echo Please ensure Python 3.10+ is installed
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo Step 3: Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Python dependencies installed
echo.

echo Step 4: Creating .env file from template...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file
    echo.
    echo IMPORTANT: Please edit .env file with your credentials:
    echo   - YOUTUBE_API_KEY
    echo   - NOTEBOOKLM_NOTEBOOK_ID
    echo   - EMAIL_SENDER
    echo   - EMAIL_PASSWORD
    echo   - EMAIL_RECIPIENT
    echo.
) else (
    echo ✓ .env file already exists
    echo.
)

echo Step 5: Creating logs directory...
if not exist logs mkdir logs
echo ✓ Logs directory ready
echo.

echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Install NotebookLM MCP CLI: npm install -g notebooklm-mcp-cli
echo 2. Edit .env file with your credentials
echo 3. Authenticate NotebookLM: nlm login
echo 4. Test run: python src\main.py
echo 5. Setup Windows Task Scheduler (see README.md)
echo.
echo See README.md for detailed instructions.
echo.

pause
