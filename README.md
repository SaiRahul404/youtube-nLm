# YouTube → NotebookLM Automation POC

Automated YouTube channel monitoring system that processes new videos through NotebookLM and emails AI-generated insights.

## 🎯 Overview

This POC automatically:
1. Monitors the MoneyPurse YouTube channel for new uploads
2. Adds new videos as sources to a NotebookLM notebook
3. Runs AI analysis on the video content
4. Emails the insights to a specified recipient

## 📋 Prerequisites

- **Python 3.10+** (required for NotebookLM CLI compatibility)
- **Chrome Browser** (required for NotebookLM authentication)
- **Node.js & npm** (for NotebookLM MCP CLI)
- **YouTube Data API v3 Key**
- **NotebookLM Account** and Notebook ID
- **Email Account** (Gmail with App Password recommended)

## 🚀 Setup Instructions

### 1. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install NotebookLM MCP CLI

```bash
npm install -g notebooklm-mcp-cli
```

### 3. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **YouTube Data API v3**
4. Create credentials → API Key
5. Copy the API key

### 4. Get NotebookLM Notebook ID

1. Go to [NotebookLM](https://notebooklm.google.com/)
2. Create or open a notebook
3. The Notebook ID is in the URL: `https://notebooklm.google.com/notebook/{NOTEBOOK_ID}`
4. Copy the Notebook ID

### 5. Configure Email (Gmail Example)

**For Gmail:**
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate app password for "Mail"
5. Copy the 16-character password

**For other providers:**
- Update SMTP server and port in `.env` file

### 6. Create Environment Configuration

```bash
# Copy example file
copy .env.example .env

# Edit .env with your credentials
notepad .env
```

Fill in all the required values:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_CHANNEL_USERNAME=@MoneyPurse
NOTEBOOKLM_NOTEBOOK_ID=your_notebook_id_here
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=465
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENT=recipient@example.com
NOTEBOOKLM_PROMPT=Analyze this video and provide key insights, takeaways, and actionable recommendations.
```

### 7. Authenticate NotebookLM CLI

```bash
nlm login
```

This will open Chrome for authentication. Complete the login process.

⚠️ **Important**: NotebookLM sessions expire frequently (~20 minutes). The script automatically re-authenticates when needed.

### 8. Test Manual Run

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the script
python src\main.py
```

Check `logs/automation.log` for execution details.

## 🤖 Windows Task Scheduler Setup

### Automated Setup (Recommended)

Simply run the setup script:

```bash
# Double-click to run:
setup_scheduler.bat

# Or run in PowerShell as Administrator:
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1
```

This will:
- Create a scheduled task named `YouTube_NotebookLM_Automation`
- Run every **12 hours** (8:00 AM and 8:00 PM daily)
- Execute even if not logged in or on battery
- Enable automatic restart on failure

### Remove Scheduled Task

To remove the scheduled task:

```bash
# Double-click to run:
remove_scheduler.bat

# Or run in PowerShell as Administrator:
powershell -ExecutionPolicy Bypass -File remove_scheduler.ps1
```

### Manual Setup (Alternative)

If you prefer manual configuration:

1. Open **Task Scheduler** (`taskschd.msc`)
2. Click **Create Task**
3. **General Tab:**
   - Name: `YouTube NotebookLM Automation`
   - ✅ Run whether user is logged on or not
   - ✅ Run with highest privileges
4. **Triggers Tab:**
   - Click **New** → **Daily** at 8:00 AM
   - Repeat task every: **12 hours**
   - Duration: **1 day**
5. **Actions Tab:**
   - Start a program: `C:\Users\rahulg_500325\Documents\NLM\run_automation.bat`
6. **Settings Tab:**
   - ✅ Allow task to be run on demand
   - ✅ Run task as soon as possible after a scheduled start is missed

### Test the Scheduled Task

```powershell
# Test the task manually
Start-ScheduledTask -TaskName "YouTube_NotebookLM_Automation"

# Check task status
Get-ScheduledTask -TaskName "YouTube_NotebookLM_Automation" | Get-ScheduledTaskInfo
```

Check logs to verify execution.

## 📁 Project Structure

```
NLM/
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── main.py                   # Main orchestration script
│   ├── youtube_monitor.py        # YouTube API integration
│   ├── state_manager.py          # State tracking
│   ├── notebooklm_handler.py     # NotebookLM CLI integration
│   └── email_sender.py           # Email notifications
├── logs/
│   └── automation.log            # Execution logs
├── .env                          # Environment variables (create from .env.example)
├── .env.example                  # Example configuration
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── run_automation.bat            # Windows Task Scheduler wrapper
├── README.md                     # This file
├── PRD.md                        # Product Requirements Document
└── plan-youtubeToNotebookLmAutomation.prompt.md  # Implementation plan
```

## 🔍 Monitoring & Troubleshooting

### Check Logs

```bash
# View recent logs
type logs\automation.log

# Monitor logs in real-time (PowerShell)
Get-Content logs\automation.log -Wait -Tail 20
```

### Common Issues

**1. NotebookLM Authentication Fails**
- Ensure Chrome is installed and accessible
- Run `nlm login` manually to re-authenticate
- Check if Task Scheduler has proper permissions

**2. YouTube API Errors**
- Verify API key is correct
- Check quota limits in Google Cloud Console
- Ensure YouTube Data API v3 is enabled

**3. Email Sending Fails**
- Verify app password (not regular password)
- Check SMTP server and port settings
- Ensure "Less secure app access" is NOT needed (use App Password instead)

**4. No New Videos Detected**
- Check channel username format (`@MoneyPurse`)
- Verify channel has recent uploads
- Check state file: `.youtube_notebooklm/processed_videos.json`

### Reset State

To reprocess videos:
```bash
# Delete state file
del %USERPROFILE%\.youtube_notebooklm\processed_videos.json
```

## ⚠️ Important Limitations

### NotebookLM Rate Limits
- **~50 queries/day** on free tier (approximately 25 videos/day)
- Recommended polling interval: **1-2 hours**
- Script processes one video at a time

### Authentication Brittleness
- NotebookLM sessions expire frequently
- Script auto-retries authentication
- May fail in Task Scheduler context without GUI access
- **Test thoroughly** before production use

### Unofficial API
- `notebooklm-mcp-cli` uses undocumented APIs
- Could break without notice
- Monitor for updates regularly

## 🧪 Testing Checklist

- [ ] Manual script run completes successfully
- [ ] YouTube API connects and finds videos
- [ ] NotebookLM authentication works
- [ ] Video source is added to notebook
- [ ] NotebookLM query returns analysis
- [ ] Email is received successfully
- [ ] State file is created and updated
- [ ] Task Scheduler runs successfully
- [ ] Logs show no errors
- [ ] Test with 2-3 new videos

## 📝 Configuration Tips

### Custom Prompts

Edit the `NOTEBOOKLM_PROMPT` in `.env`:

```
NOTEBOOKLM_PROMPT=Provide a detailed summary of this video including: 1) Main topic, 2) Key arguments, 3) Supporting evidence, 4) Conclusions, 5) Actionable insights for investors.
```

### Multiple Recipients

For multiple email recipients, modify `email_sender.py` to accept a list of recipients.

### Different YouTube Channel

Change `YOUTUBE_CHANNEL_USERNAME` in `.env`:

```
YOUTUBE_CHANNEL_USERNAME=@YourChannel
```

## 🔄 Maintenance

### Weekly
- Check logs for errors
- Verify emails are being received
- Monitor NotebookLM quota usage

### Monthly
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Check for `notebooklm-mcp-cli` updates: `npm update -g notebooklm-mcp-cli`
- Review processed videos in state file

## 📞 Support

For issues or questions:
1. Check logs first: `logs/automation.log`
2. Review this README
3. Check the plan file: `plan-youtubeToNotebookLmAutomation.prompt.md`

## 📄 License

This is a Proof of Concept (POC) project for personal use.

---

**Built with:** Python, YouTube Data API v3, NotebookLM MCP CLI, Windows Task Scheduler
