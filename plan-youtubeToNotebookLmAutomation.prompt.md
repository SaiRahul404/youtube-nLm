# Plan: YouTube → NotebookLM Automation POC

This POC will build a Python automation script to monitor the MoneyPurse YouTube channel, process new videos through NotebookLM, and email AI-generated insights. The system uses the `notebooklm-mcp-cli` tool, YouTube Data API v3, and standard email libraries. Key constraint: NotebookLM's ~50 queries/day limit means processing ~1 video/hour maximum. Authentication relies on Chrome browser availability, which adds complexity to Task Scheduler execution.

## Steps

### 1. Project Setup & Dependencies
- Create Python project structure with main script, config module, and utilities
- Install dependencies: `notebooklm-mcp-cli`, `google-api-python-client`, `filelock`
- Python 3.10+ required for NotebookLM CLI compatibility
- Ensure Chrome browser installed and accessible in PATH

### 2. Configuration Management
- Create `config.py` to store: YouTube API key, channel ID/username (@MoneyPurse), NotebookLM notebook ID, email credentials (SMTP server, port, sender/recipient addresses), prompt template, state file path
- Use environment variables or separate `.env` file for sensitive credentials (API keys, passwords)
- Document Gmail App Password requirement (if using Gmail SMTP)

### 3. YouTube Monitoring Module (`youtube_monitor.py`)
- Initialize YouTube Data API v3 client with API key
- Implement one-time channel lookup to get uploads playlist ID (cache this in state file)
- Create `check_for_new_videos()` function that polls `playlistItems.list` endpoint (1 API unit/call)
- Extract video IDs, titles, and publish timestamps from API response
- Return list of new videos not in processed state

### 4. State Management Module (`state_manager.py`)
- Implement JSON state file at `~/.youtube_notebooklm/processed_videos.json`
- Structure: `{processed_videos: [{video_id, title, published_at, processed_at, notebook_id, status}], last_check, channel_uploads_playlist_id}`
- Use `filelock` library to prevent concurrent access issues
- Functions: `load_state()`, `save_state()`, `is_processed(video_id)`, `mark_processed(video_id, metadata)`
- Implement state file backup/corruption recovery

### 5. NotebookLM Integration Module (`notebooklm_handler.py`)
- Implement `ensure_authenticated()` helper that checks auth status via `nlm login --check` and re-authenticates if needed
- Create `process_video(video_url, prompt)` function
- Add video as source: `nlm source add <notebook_id> --url <video_url>`
- Run query: `nlm notebook query <notebook_id> "<prompt>"`
- Capture and parse stdout response
- Wrap all CLI calls with retry logic (3 attempts with exponential backoff) for transient failures
- Handle authentication errors specifically - re-run `nlm login` and retry operation

### 6. Email Notification Module (`email_sender.py`)
- Use standard library `smtplib` with `email.mime` for message construction
- Create `send_email(subject, body, recipient)` function
- Format email with video title, URL, and NotebookLM analysis
- Support both plain text and HTML formatting
- Configure for Gmail (smtp.gmail.com:465 with SSL) or alternative SMTP provider
- Implement error handling for SMTP connection failures

### 7. Main Orchestration Script (`main.py`)
- Implement main workflow: check YouTube → compare with state → process new videos → send emails → update state
- Add comprehensive logging using Python `logging` module (file + console output)
- Error handling strategy: log all errors, continue processing remaining videos even if one fails
- For each new video: authenticate NotebookLM → add source → run query → send email → mark as processed
- Implement graceful degradation: if NotebookLM fails, still mark video as attempted (with error status) to avoid retry loops

### 8. Windows Task Scheduler Configuration
- Create batch script wrapper (`run_automation.bat`) to activate virtual environment and run Python script
- Configure Task Scheduler trigger for periodic execution (recommended: every 1-2 hours to respect NotebookLM rate limits)
- Settings: "Run whether user is logged on or not", "Run with highest privileges", "Allow task to be run on demand"
- Important: Test that Chrome browser is accessible in Task Scheduler execution context (may need user-level task, not system-level)

### 9. Testing & Validation
- Manual test: Run script once to verify YouTube API connectivity and channel resolution
- Test NotebookLM authentication in Task Scheduler context (critical blocker)
- Test email delivery with sample message
- Dry-run with existing videos (mark as processed without actually processing)
- Monitor first 24 hours for auth expiration and re-authentication success
- Verify state file updates correctly after processing

## Verification

- Run script manually and confirm log file shows successful YouTube API connection, new video detection, NotebookLM processing, email delivery
- Check state JSON file contains processed video entries with timestamps
- Verify email received with formatted NotebookLM response
- Test Task Scheduler execution: confirm task runs successfully, check logs for any permission/authentication issues
- Monitor for 48 hours to verify authentication resilience and re-login automation
- Test edge cases: no new videos, API failures, authentication expiration mid-run

## Decisions

- **Chose `notebooklm-mcp-cli` over deprecated `notebooklm-cli`** - the active maintained version with unified functionality
- **YouTube API polling over webhooks** - simpler for POC, no server infrastructure required
- **Local JSON state over database** - meets "no database" requirement from PRD, sufficient for single channel monitoring
- **Standard `smtplib` over third-party email services** - no additional dependencies, works with any SMTP provider
- **Cron/Task Scheduler over continuous service** - matches user preference, better for rate limit management
- **1-2 hour polling interval** - balances timely detection with NotebookLM's ~50 queries/day limit

## Critical Risks to Monitor

⚠️ **Authentication Brittleness**: NotebookLM sessions expire every ~20 minutes; the CLI needs Chrome browser access. Task Scheduler execution context may not have GUI access for automated re-login. Test thoroughly before deployment.

⚠️ **Rate Limits**: NotebookLM free tier allows ~50 queries/day (≈25 videos/day). If MoneyPurse uploads more frequently, implement queue/prioritization.

⚠️ **Unofficial API**: `notebooklm-mcp-cli` uses undocumented internal APIs that could break without notice. Have fallback plan (manual processing or alternative tools).
