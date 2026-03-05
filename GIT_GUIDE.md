# Git Setup and Push Guide

## Quick Start

```bash
# 1. Initialize Git repository
git init

# 2. Add all files (respects .gitignore)
git add .

# 3. Check what will be committed
git status

# 4. Create initial commit
git commit -m "Initial commit: YouTube NotebookLM Automation POC"

# 5. Add remote repository
git remote add origin <your-repo-url>

# 6. Push to remote
git push -u origin main
```

## What Gets Pushed? ✅

The following files **WILL** be pushed to Git:

### Core Code
- `src/*.py` - All Python source code
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template (safe)

### Scripts
- `setup.bat` - Virtual environment setup
- `run_automation.bat` - Execution wrapper
- `setup_scheduler.bat` - Task scheduler setup
- `setup_scheduler.ps1` - PowerShell scheduler script
- `remove_scheduler.bat` - Remove task script
- `remove_scheduler.ps1` - Remove task PowerShell script
- `authenticate_notebooklm.py` - Authentication helper
- `test_channel_lookup.py` - Testing utility

### Documentation
- `README.md` - Main documentation
- `GETTING_STARTED.md` - Quick start guide
- `QUICK_REFERENCE.md` - Command reference
- `TASK_SCHEDULER_GUIDE.md` - Scheduler guide
- `PRD.md` - Product requirements
- `plan-youtubeToNotebookLmAutomation.prompt.md` - Implementation plan

### Configuration
- `.gitignore` - Git ignore rules

## What Gets IGNORED? ❌

The following files **WILL NOT** be pushed (for good reasons):

### Sensitive Data
- `.env` - Contains API keys and passwords (NEVER PUSH!)
- `.youtube_notebooklm/` - Contains state and processed video IDs

### Generated Files
- `venv/` - Virtual environment (150+ MB, user-specific)
- `logs/` - Log files (can be regenerated)
- `__pycache__/` - Python bytecode cache
- `node_modules/` - Node.js dependencies (if any)

### OS/IDE Files
- `.vscode/`, `.idea/` - IDE settings
- `.DS_Store`, `Thumbs.db` - OS metadata files

## Important Security Notes ⚠️

### Before Pushing: Verify No Secrets

```bash
# Check if .env is excluded
git status

# Search for potential secrets (should return nothing)
git grep -i "api.key"
git grep -i "password"
```

### If You Accidentally Committed Secrets

```bash
# Remove from Git history (if just committed)
git reset HEAD~1

# Or remove specific file from staging
git reset HEAD .env

# Remove from Git history completely (if already pushed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

## Common Git Commands

### Check Status
```bash
# See what's changed
git status

# See what's being ignored
git status --ignored
```

### View Changes
```bash
# See unstaged changes
git diff

# See staged changes
git diff --cached
```

### Commit More Changes
```bash
git add .
git commit -m "Your commit message"
git push
```

### Update from Remote
```bash
# Pull latest changes
git pull origin main
```

### Branch Management
```bash
# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name
```

## Setup for GitHub/GitLab/Bitbucket

### GitHub
1. Create new repository on GitHub
2. Copy the repository URL
3. Run:
   ```bash
   git remote add origin https://github.com/username/repo-name.git
   git branch -M main
   git push -u origin main
   ```

### GitLab
1. Create new project on GitLab
2. Copy the repository URL
3. Run:
   ```bash
   git remote add origin https://gitlab.com/username/repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Bitbucket
1. Create new repository on Bitbucket
2. Copy the repository URL
3. Run:
   ```bash
   git remote add origin https://bitbucket.org/username/repo-name.git
   git branch -M main
   git push -u origin main
   ```

## Checklist Before First Push ✓

- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` exists with dummy values
- [ ] No sensitive data in any committed files
- [ ] `venv/` is excluded
- [ ] `logs/` is excluded
- [ ] All required files are included
- [ ] README.md is complete and accurate

## Verify .gitignore is Working

```bash
# This should NOT show .env or venv/ or logs/
git status

# Force check what's being tracked
git ls-files
```

## Clone Instructions (for others)

After pushing, others can clone and set up with:

```bash
# Clone repository
git clone <repo-url>
cd NLM

# Copy and configure environment
copy .env.example .env
# Edit .env with actual credentials

# Setup Python environment
setup.bat

# Activate virtual environment
venv\Scripts\activate

# Install NotebookLM CLI
npm install -g notebooklm-mcp-cli

# Test configuration
python src\main.py

# Setup automation (optional)
setup_scheduler.bat
```

## Tips

1. **Never force push** unless you know what you're doing
2. **Always pull before push** to avoid conflicts
3. **Write meaningful commit messages**
4. **Commit small, logical changes** rather than huge batches
5. **Review changes before committing**: `git diff`
6. **Keep sensitive data out of Git** - use .env files
