# YouTube NotebookLM Automation - Task Scheduler Removal
# Run this script as Administrator to remove the scheduled task

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Remove YouTube NotebookLM Automation" -ForegroundColor Cyan
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

$taskName = "YouTube_NotebookLM_Automation"

# Check if task exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if (-not $existingTask) {
    Write-Host "Task '$taskName' not found. Nothing to remove." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 0
}

Write-Host "Found scheduled task: $taskName" -ForegroundColor Green
Write-Host ""
Write-Host "This will remove the automated task from Task Scheduler." -ForegroundColor Yellow
$confirm = Read-Host "Are you sure you want to remove it? (y/n)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    try {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host ""
        Write-Host "SUCCESS! Task removed successfully." -ForegroundColor Green
        Write-Host ""
    } catch {
        Write-Host ""
        Write-Host "ERROR: Failed to remove task" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "Cancelled. Task was not removed." -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Press Enter to exit"
