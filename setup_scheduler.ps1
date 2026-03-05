# YouTube NotebookLM Automation - Task Scheduler Setup
# Run this script as Administrator

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "YouTube NotebookLM Automation Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Define task parameters
$taskName = "YouTube_NotebookLM_Automation"
$scriptPath = "$PSScriptRoot\run_automation.bat"
$startTime = "08:00AM"

# Check if bat file exists
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: run_automation.bat not found at: $scriptPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Configuration:" -ForegroundColor Green
Write-Host "  Task Name: $taskName"
Write-Host "  Script: $scriptPath"
Write-Host "  Frequency: Every 12 hours"
Write-Host "  Start Time: $startTime (daily)"
Write-Host ""

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create scheduled task action
Write-Host "Creating scheduled task..." -ForegroundColor Cyan
$action = New-ScheduledTaskAction -Execute $scriptPath

# Create trigger - Daily at 8 AM, repeat every 12 hours for 24 hours
$trigger = New-ScheduledTaskTrigger -Daily -At $startTime
$trigger.Repetition = (New-ScheduledTaskTrigger -Once -At $startTime -RepetitionInterval (New-TimeSpan -Hours 12) -RepetitionDuration (New-TimeSpan -Days 1)).Repetition

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Monitors YouTube channel for new videos and sends AI-powered analysis emails every 12 hours" `
        -User $env:USERNAME `
        -RunLevel Highest `
        -ErrorAction Stop
    
    Write-Host ""
    Write-Host "SUCCESS! Task scheduled successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor Cyan
    Write-Host "  - Runs every 12 hours starting at $startTime"
    Write-Host "  - Executions: 8:00 AM and 8:00 PM daily"
    Write-Host "  - Will run even if on battery power"
    Write-Host "  - Maximum runtime: 1 hour per execution"
    Write-Host ""
    Write-Host "To verify the task:" -ForegroundColor Yellow
    Write-Host "  1. Open Task Scheduler (taskschd.msc)"
    Write-Host "  2. Look for '$taskName' in Task Scheduler Library"
    Write-Host ""
    Write-Host "To test now:" -ForegroundColor Yellow
    Write-Host "  Start-ScheduledTask -TaskName '$taskName'"
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"
