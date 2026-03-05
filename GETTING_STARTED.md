# Getting Started - Step by Step Guide

Follow these steps in order to set up the YouTube NotebookLM automation.

---

## Step 1: Install Required Software

### Check if Python is installed
1. Open PowerShell or Command Prompt
2. Type: `python --version`
3. You should see Python 3.10 or higher
4. **If not installed**: Download from [python.org](https://www.python.org/downloads/)

### Check if Node.js is installed
1. In PowerShell, type: `node --version`
2. You should see a version number
3. **If not installed**: Download from [nodejs.org](https://nodejs.org/)

### Make sure Chrome is installed
- The NotebookLM CLI requires Chrome browser
- Download from [google.com/chrome](https://www.google.com/chrome/) if needed

---

## Step 2: Run the Setup Script

1. Navigate to this folder in File Explorer: `C:\Users\rahulg_500325\Documents\NLM`
2. Double-click on **`setup.bat`**
3. Wait for it to complete - this will:
   - Create a Python virtual environment
   - Install all Python dependencies
   - Create a `.env` file for your settings

---

## Step 3: Get Your YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"** (or select existing one)
3. Give it a name like "YouTube Automation"
4. Click **"APIs & Services"** → **"Enable APIs and Services"**
5. Search for **"YouTube Data API v3"**
6. Click **"Enable"**
7. Go to **"Credentials"** → **"Create Credentials"** → **"API Key"**
8. **Copy the API key** - you'll need it in Step 6

---

## Step 4: Get Your NotebookLM Notebook ID

1. Go to [NotebookLM](https://notebooklm.google.com/)
2. Sign in with your Google account
3. Create a new notebook or open an existing one
4. Look at the URL in your browser, it looks like:
   ```
   https://notebooklm.google.com/notebook/abc123def456
   ```
5. **Copy the ID part** (the `abc123def456` part after `/notebook/`)

---

## Step 5: Get Your Gmail App Password

### If using Gmail:

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Make sure **"2-Step Verification"** is turned ON
   - If not, turn it on first
3. Search for **"App passwords"** in the settings
4. Click **"App passwords"**
5. Select app: **"Mail"**
6. Select device: **"Windows Computer"**
7. Click **"Generate"**
8. **Copy the 16-character password** (it looks like: `abcd efgh ijkl mnop`)

### If using another email:
- You'll need your SMTP server address and port
- For example, Outlook uses `smtp.office365.com` and port `587`

---

## Step 6: Configure the .env File

1. In the `NLM` folder, find the file named **`.env`**
2. Right-click it and open with **Notepad**
3. Fill in your information:

```
YOUTUBE_API_KEY=paste_your_youtube_api_key_here
YOUTUBE_CHANNEL_USERNAME=@MoneyPurse
NOTEBOOKLM_NOTEBOOK_ID=paste_your_notebook_id_here
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=465
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=paste_your_16_character_app_password_here
EMAIL_RECIPIENT=where_to_send_notifications@example.com
NOTEBOOKLM_PROMPT=Analyze this video and provide key insights, takeaways, and actionable recommendations.
```

4. **Save the file** (Ctrl + S)

---

## Step 7: Install NotebookLM CLI

1. Open PowerShell
2. Run this command:
   ```
   npm install -g notebooklm-mcp-cli
   ```
3. Wait for installation to complete

---

## Step 8: Login to NotebookLM CLI

### Option 1: Use the Authentication Helper (Recommended)

1. In PowerShell (with venv activated), run:
   ```
   python authenticate_notebooklm.py
   ```
2. Press Enter when prompted
3. Chrome will open automatically
4. Sign in with your Google account
5. Grant permissions when asked
6. Chrome will close automatically
7. You should see "✓ Authentication complete!"

### Option 2: Manual Authentication

1. In PowerShell, run:
   ```
   nlm login
   ```
2. If you see encoding errors, ignore them - the authentication still works
3. Chrome will open - sign in and grant permissions
4. Check if it worked:
   ```
   nlm login --check
   ```
5. You should see "authenticated" in the output

**Note:** If you see Unicode character errors during authentication, that's normal on Windows - the authentication still succeeds!

---

## Step 9: Test the Automation

### First: Test Channel Lookup (Recommended)

Before running the full automation, test that your YouTube channel can be found:

1. In PowerShell (with venv activated), run:
   ```
   python test_channel_lookup.py
   ```

2. This will:
   - Search for the channel
   - Show all matching channels with subscriber counts
   - Let you verify which one is correct
   - Test that videos can be retrieved

3. If it asks you to select a channel, choose the correct one

4. If successful, it will show the Channel ID - **copy this!**

5. Add to your `.env` file:
   ```
   YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxx
   ```

### Then: Run the Full Script

1. Open PowerShell
2. Navigate to the project folder:
   ```
   cd C:\Users\rahulg_500325\Documents\NLM
   ```
3. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Run the script:
   ```
   python src\main.py
   ```
5. Watch the output - it should:
   - Connect to YouTube
   - Find recent videos
   - Process them through NotebookLM
   - Send you an email

6. Check your email inbox for the notification!

---

## Step 10: Set Up Automatic Scheduling (Optional)

If you want this to run automatically every few hours:

1. Press **Windows Key + R**
2. Type: `taskschd.msc` and press Enter
3. Click **"Create Task"** (not "Create Basic Task")
4. In the **General** tab:
   - Name: `YouTube NotebookLM Automation`
   - Check: ☑ "Run whether user is logged on or not"
   - Check: ☑ "Run with highest privileges"

5. In the **Triggers** tab:
   - Click **"New"**
   - Begin the task: "On a schedule"
   - Choose: **Daily**
   - Repeat task every: **2 hours**
   - For a duration of: **Indefinitely**
   - Click **OK**

6. In the **Actions** tab:
   - Click **"New"**
   - Action: "Start a program"
   - Program/script: `C:\Users\rahulg_500325\Documents\NLM\run_automation.bat`
   - Start in: `C:\Users\rahulg_500325\Documents\NLM`
   - Click **OK**

7. In the **Settings** tab:
   - Check: ☑ "Allow task to be run on demand"
   - Check: ☑ "Run task as soon as possible after a scheduled start is missed"

8. Click **OK** to save
9. Enter your Windows password when prompted

---

## ✅ You're Done!

The system will now:
- Check for new videos every 2 hours (if you set up Task Scheduler)
- Process them through NotebookLM
- Email you the AI analysis

---

## 🆘 Troubleshooting

### Problem: "Python not found"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

### Problem: "npm is not recognized"
- Install Node.js from nodejs.org
- Restart PowerShell after installation

### Problem: NotebookLM login fails or shows encoding errors
- **Unicode encoding errors during `nlm login` are NORMAL on Windows** - ignore them!
- The authentication still succeeds even if you see errors
- Use the helper script instead: `python authenticate_notebooklm.py`
- Make sure Chrome is installed
- Check if you're already logged in: `nlm login --check`
- If it says "authenticated", you're good to go!
- Check that you're signing in with the correct Google account

### Problem: Email not sending
- Double-check your app password (16 characters, no spaces)
- Make sure 2-Step Verification is enabled
- Try generating a new app password

### Problem: YouTube API error or "Channel not found"
- Run the test script: `python test_channel_lookup.py`
- This will help you find the correct channel ID
- Add the channel ID to your `.env` file:
  ```
  YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxx
  ```
- Make sure you copied the API key correctly
- Check that YouTube Data API v3 is enabled in Google Cloud Console
- Make sure you didn't exceed the free tier quota

### Problem: Unicode/Encoding errors
- This is now fixed in the code
- If you still see errors, the logs will still be saved to the file correctly
- Only console display might show some `?` for emojis

### Check the logs
If something doesn't work, look at the log file:
```
C:\Users\rahulg_500325\Documents\NLM\logs\automation.log
```

Open it with Notepad to see what went wrong.

---

## 📞 Need More Help?

- Read the full README.md for more details
- Check QUICK_REFERENCE.md for common commands
- Look at the logs folder for error messages
