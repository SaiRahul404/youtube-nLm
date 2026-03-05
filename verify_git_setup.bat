@echo off
echo.
echo =======================================
echo   Git Repository Setup Verification
echo =======================================
echo.

:: Check if git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

:: Check if .gitignore exists
if not exist ".gitignore" (
    echo [ERROR] .gitignore file not found
    pause
    exit /b 1
)
echo [OK] .gitignore exists
echo.

:: Check if .env is in .gitignore
findstr /C:".env" .gitignore >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] .env is in .gitignore
) else (
    echo [WARNING] .env not found in .gitignore
)
echo.

:: Check if .env.example exists
if exist ".env.example" (
    echo [OK] .env.example exists
) else (
    echo [WARNING] .env.example not found - create it as a template
)
echo.

:: Check for sensitive files
echo Checking for sensitive files...
if exist ".env" (
    echo [OK] .env exists locally (will be ignored by Git)
) else (
    echo [WARNING] .env file not found - needed for running the project
)
echo.

echo =======================================
echo   Files that WILL be committed:
echo =======================================
echo.
echo Source Code:
echo   - src\*.py
echo   - requirements.txt
echo.
echo Scripts:
echo   - *.bat, *.ps1 files
echo   - test_channel_lookup.py
echo   - authenticate_notebooklm.py
echo.
echo Documentation:
echo   - *.md files (README, guides, etc.)
echo.
echo Configuration:
echo   - .gitignore
echo   - .env.example
echo.
echo =======================================
echo   Files that will be IGNORED:
echo =======================================
echo.
echo   - .env (sensitive credentials)
echo   - venv\ (virtual environment)
echo   - logs\ (log files)
echo   - .youtube_notebooklm\ (state files)
echo   - __pycache__\ (Python cache)
echo.
echo =======================================

:: Initialize git if not already
if not exist ".git" (
    echo.
    echo [INFO] Git repository not initialized yet
    echo.
    set /p INIT="Do you want to initialize Git now? (y/n): "
    if /i "%INIT%"=="y" (
        git init
        echo.
        echo [OK] Git repository initialized
        echo Next steps:
        echo   1. git add .
        echo   2. git commit -m "Initial commit"
        echo   3. git remote add origin ^<your-repo-url^>
        echo   4. git push -u origin main
    )
) else (
    echo.
    echo [OK] Git repository already initialized
    echo.
    echo Current status:
    git status --short
)

echo.
echo =======================================
echo.
echo See GIT_GUIDE.md for detailed instructions
echo.
pause
