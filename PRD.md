# YouTube → NotebookLM Automation (POC)

## 1. Overview

This project is a Proof of Concept (POC) that automates the process of monitoring a YouTube channel for new uploads and generating AI insights from those videos using NotebookLM.

When a new video is uploaded to the monitored channel, the system will:

1. Detect the new video
2. Add the video URL as a source to a NotebookLM notebook
3. Run a predefined prompt in NotebookLM
4. Capture the response
5. Send the response via email

The goal is to build a simple automation pipeline that acts as a personal AI research assistant for YouTube content.

---

# 2. Objective

Build a simple automation script that:

- Monitors a specific YouTube channel
- Detects newly uploaded videos
- Adds the video link to NotebookLM
- Runs a predefined prompt
- Sends the AI-generated result via email

This POC validates the feasibility of integrating YouTube monitoring with NotebookLM automation.

---

# 3. Scope

This POC will support:

- One YouTube channel
- One NotebookLM notebook
- One fixed prompt
- One email recipient
- Local machine execution
- No database usage

---

# 4. Target YouTube Channel

The system will monitor the following channel:

https://www.youtube.com/@MoneyPurse

The system will detect newly uploaded videos from this channel.

---

# 5. High-Level Workflow
