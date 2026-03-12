# Quick Reference Guide

## Quick Start

```bash
# 1. Run setup
setup.bat

# 2. Edit configuration
notepad .env

# 3. Install NotebookLM CLI
npm install -g notebooklm-mcp-cli

# 4. Authenticate NotebookLM
nlm login

# 5. Test run
venv\Scripts\activate
python src\main.py
```

## Common Commands

### Run Automation Manually
```bash
# Activate environment
venv\Scripts\activate

# Run script
python src\main.py

# Or use batch file
run_automation.bat
```

### Check Logs
```bash
# View all logs
type logs\automation.log

# View last 20 lines
powershell Get-Content logs\automation.log -Tail 20

# Monitor live
powershell Get-Content logs\automation.log -Wait -Tail 20
```

### NotebookLM CLI Commands
```bash
# Login (recommended: use helper script)
python authenticate_notebooklm.py

# Login (direct command - may show encoding errors but still works)
nlm login

# Check authentication status
nlm login --check

# List sources in notebook
nlm source list YOUR_NOTEBOOK_ID --json

# Add source to notebook (script auto-clears old sources first)
nlm source add YOUR_NOTEBOOK_ID --url "https://www.youtube.com/watch?v=VIDEO_ID"

# Delete a source
nlm source delete SOURCE_ID --confirm

# Query notebook
nlm notebook query YOUR_NOTEBOOK_ID "Your prompt here"

# Test source management
python test_source_management.py
```

### State Management
```bash
# View state file
type %USERPROFILE%\.youtube_notebooklm\processed_videos.json

# Reset state (reprocess all videos)
del %USERPROFILE%\.youtube_notebooklm\processed_videos.json
```

### Task Scheduler
```bash
# Open Task Scheduler
taskschd.msc

# Run task manually
schtasks /run /tn "YouTube NotebookLM Automation"

# Check task status
schtasks /query /tn "YouTube NotebookLM Automation"
```

## Troubleshooting

### Update Dependencies
```bash
# Activate environment
venv\Scripts\activate

# Update Python packages
pip install --upgrade -r requirements.txt

# Update NotebookLM CLI
npm update -g notebooklm-mcp-cli
```

### Clear Python Cache
```bash
# Remove cache files
del /s /q src\__pycache__
rmdir /s /q src\__pycache__
```

### Reinstall Environment
```bash
# Delete virtual environment
rmdir /s /q venv

# Run setup again
setup.bat
```

## Configuration Examples

### Custom Prompt
Edit `.env`:
```
NOTEBOOKLM_PROMPT=Create a comprehensive summary including: key topics, main arguments, supporting evidence, conclusions, and actionable insights specifically for financial investors.
```

### Different Channel
Edit `.env`:
```
YOUTUBE_CHANNEL_USERNAME=@YourFavoriteChannel
```

### Different Email Provider
Edit `.env`:
```
EMAIL_SMTP_SERVER=smtp.office365.com
EMAIL_SMTP_PORT=587
```

## Testing Checklist

- [ ] Python 3.10+ installed: `python --version`
- [ ] Virtual environment created: `venv\Scripts\activate`
- [ ] Dependencies installed: `pip list`
- [ ] NotebookLM CLI installed: `nlm --version`
- [ ] NotebookLM authenticated: `nlm login --check`
- [ ] .env file configured
- [ ] Manual run successful: `python src\main.py`
- [ ] Logs created: `logs\automation.log`
- [ ] Email received
- [ ] State file created: `%USERPROFILE%\.youtube_notebooklm\processed_videos.json`
- [ ] Task Scheduler configured and tested

## Rate Limits

### NotebookLM
- **~50 queries/day** (free tier)
- ~25 videos/day with 2 queries per video
- Recommended interval: **2 hours** (12 videos/day)

### YouTube API
- **10,000 units/day** (free tier)
- Checking for videos: 1 unit per call
- Can check thousands of times per day

## File Locations

- **Project**: `C:\Users\rahulg_500325\Documents\NLM`
- **Virtual Environment**: `C:\Users\rahulg_500325\Documents\NLM\venv`
- **Logs**: `C:\Users\rahulg_500325\Documents\NLM\logs\automation.log`
- **State File**: `%USERPROFILE%\.youtube_notebooklm\processed_videos.json`
- **Configuration**: `C:\Users\rahulg_500325\Documents\NLM\.env`

## Emergency Commands

### Stop All Processing
```bash
# Kill Python processes
taskkill /IM python.exe /F

# Disable Task Scheduler task
schtasks /change /tn "YouTube NotebookLM Automation" /disable
```

### Backup State
```bash
copy %USERPROFILE%\.youtube_notebooklm\processed_videos.json processed_videos_backup.json
```

### Clean Logs
```bash
# Archive old logs
move logs\automation.log logs\automation_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log

# Or delete
del logs\automation.log
```
