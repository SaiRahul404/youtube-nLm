# Task Scheduler Quick Reference

## Setup Automation (12-hour intervals)

**Easy Way:**
1. Double-click **`setup_scheduler.bat`**
2. Click "Yes" when prompted for administrator access
3. Done! The task will run at 8:00 AM and 8:00 PM daily

**PowerShell Way:**
```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1
```

## Test the Task Manually

```powershell
# Run the task immediately
Start-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Check task status
Get-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# View task info (last run time, next run time, etc.)
Get-ScheduledTask -TaskName "YouTube_NotebookLM_Automation" | Get-ScheduledTaskInfo
```

## View Task in Task Scheduler GUI

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Look for **YouTube_NotebookLM_Automation** in Task Scheduler Library
3. Right-click → **Run** to test manually
4. Check **History** tab to see execution logs

## Check Execution Logs

```powershell
# View latest logs
Get-Content logs\automation.log -Tail 50

# Monitor logs in real-time
Get-Content logs\automation.log -Wait -Tail 20
```

## Change Schedule

### Option 1: Remove and Recreate
1. Run `remove_scheduler.bat`
2. Edit `setup_scheduler.ps1` (change `$startTime` or repetition interval)
3. Run `setup_scheduler.bat` again

### Option 2: Edit Manually in Task Scheduler
1. Open Task Scheduler (`taskschd.msc`)
2. Find **YouTube_NotebookLM_Automation**
3. Right-click → **Properties**
4. Go to **Triggers** tab → Edit trigger
5. Modify the schedule as needed

## Remove Automation

**Easy Way:**
1. Double-click **`remove_scheduler.bat`**
2. Type `y` and press Enter to confirm
3. Done!

**PowerShell Way:**
```powershell
# Run as Administrator
powershell -ExecutionPolicy Bypass -File remove_scheduler.ps1
```

## Current Configuration

- **Task Name:** YouTube_NotebookLM_Automation
- **Frequency:** Every 12 hours
- **Schedule:** 8:00 AM and 8:00 PM daily
- **Script:** run_automation.bat
- **Max Runtime:** 1 hour per execution
- **Processes:** 1 video per run (POC configuration)

## Troubleshooting

### Task doesn't run at scheduled time
```powershell
# Check if task is enabled
Get-ScheduledTask -TaskName "YouTube_NotebookLM_Automation" | Select State

# If disabled, enable it
Enable-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"
```

### Task runs but no emails received
1. Check `logs\automation.log` for errors
2. Verify `.env` file has correct credentials
3. Test manually: `python src\main.py`

### Task not found after setup
- Make sure you ran `setup_scheduler.bat` **as Administrator**
- Check for error messages during setup

## Quick Commands Cheat Sheet

```powershell
# View all scheduled tasks
Get-ScheduledTask

# Get specific task details
Get-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Run task now
Start-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Stop running task
Stop-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Enable task
Enable-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Disable task (keeps settings but stops execution)
Disable-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Remove task completely
Unregister-ScheduledTask -TaskName "YouTube_NotebookLM_Automation" -Confirm:$false
```
