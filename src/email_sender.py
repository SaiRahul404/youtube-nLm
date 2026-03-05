"""Email notification module."""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)


class EmailSender:
    """Send email notifications."""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str
    ):
        """
        Initialize email sender.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            sender_email: Sender email address
            sender_password: Sender email password (or app password)
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def _create_html_message(
        self,
        video_title: str,
        video_url: str,
        analysis: str
    ) -> str:
        """
        Create HTML formatted email message.
        
        Args:
            video_title: YouTube video title
            video_url: YouTube video URL
            analysis: NotebookLM analysis text
            
        Returns:
            HTML formatted message
        """
        html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                        line-height: 1.7;
                        color: #2c3e50;
                        background-color: #f5f7fa;
                        padding: 20px;
                        margin: 0;
                    }}
                    .container {{
                        max-width: 700px;
                        margin: 0 auto;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0 0 8px 0;
                        font-size: 24px;
                        font-weight: 600;
                    }}
                    .header-subtitle {{
                        margin: 0;
                        font-size: 14px;
                        opacity: 0.9;
                    }}
                    .video-info {{
                        background-color: #f8f9fa;
                        padding: 20px 30px;
                        border-bottom: 1px solid #e9ecef;
                    }}
                    .video-title {{
                        font-size: 18px;
                        font-weight: 600;
                        color: #1a1a1a;
                        margin: 0 0 15px 0;
                        line-height: 1.4;
                    }}
                    .watch-button {{
                        display: inline-block;
                        background-color: #e74c3c;
                        color: white;
                        padding: 10px 24px;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: 500;
                        font-size: 14px;
                        transition: background-color 0.2s;
                    }}
                    .watch-button:hover {{
                        background-color: #c0392b;
                    }}
                    .summary-section {{
                        padding: 30px;
                    }}
                    .summary-header {{
                        display: flex;
                        align-items: center;
                        margin-bottom: 20px;
                        padding-bottom: 15px;
                        border-bottom: 2px solid #667eea;
                    }}
                    .summary-icon {{
                        font-size: 24px;
                        margin-right: 10px;
                    }}
                    .summary-title {{
                        font-size: 20px;
                        font-weight: 600;
                        color: #667eea;
                        margin: 0;
                    }}
                    .summary-content {{
                        background-color: #f8f9fa;
                        padding: 25px;
                        border-radius: 8px;
                        border-left: 4px solid #667eea;
                        white-space: pre-wrap;
                        line-height: 1.8;
                        font-size: 15px;
                    }}
                    .footer {{
                        background-color: #2c3e50;
                        color: #ecf0f1;
                        padding: 20px 30px;
                        text-align: center;
                        font-size: 13px;
                    }}
                    .footer p {{
                        margin: 5px 0;
                    }}
                    .footer-disclaimer {{
                        opacity: 0.7;
                        font-size: 12px;
                        margin-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 Video Summary Report</h1>
                        <p class="header-subtitle">AI-Powered Content Analysis</p>
                    </div>
                    
                    <div class="video-info">
                        <div class="video-title">{video_title}</div>
                        <a href="{video_url}" class="watch-button">▶ Watch Video</a>
                    </div>
                    
                    <div class="summary-section">
                        <div class="summary-header">
                            <span class="summary-icon">📝</span>
                            <h2 class="summary-title">Summary</h2>
                        </div>
                        <div class="summary-content">{analysis}</div>
                    </div>
                    
                    <div class="footer">
                        <p><strong>Automated Video Summarizer</strong></p>
                        <p>Powered by NotebookLM AI</p>
                        <p class="footer-disclaimer">Generated automatically for informational purposes</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html
    
    def _create_text_message(
        self,
        video_title: str,
        video_url: str,
        analysis: str
    ) -> str:
        """
        Create plain text email message.
        
        Args:
            video_title: YouTube video title
            video_url: YouTube video URL
            analysis: NotebookLM analysis text
            
        Returns:
            Plain text formatted message
        """
        text = f"""
New YouTube Video Analysis
==========================

Video: {video_title}
URL: {video_url}

AI Analysis:
-----------
{analysis}

---
Generated by YouTube NotebookLM Automation
        """
        return text.strip()
    
    def send_video_analysis(
        self,
        recipient_email: str,
        video_title: str,
        video_url: str,
        analysis: str
    ) -> bool:
        """
        Send video analysis email.
        
        Args:
            recipient_email: Recipient email address
            video_title: YouTube video title
            video_url: YouTube video URL
            analysis: NotebookLM analysis text
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"� Video Summary: {video_title}"
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            # Create plain text and HTML versions
            text_content = self._create_text_message(video_title, video_url, analysis)
            html_content = self._create_html_message(video_title, video_url, analysis)
            
            # Attach both versions
            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            logger.info(f"Sending email to {recipient_email}")
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info("Email sent successfully")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            logger.error("Check your email credentials and app password")
            return False
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_simple_email(
        self,
        recipient_email: str,
        subject: str,
        body: str
    ) -> bool:
        """
        Send a simple plain text email.
        
        Args:
            recipient_email: Recipient email address
            subject: Email subject
            body: Email body text
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            msg = MIMEText(body, "plain")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            logger.info(f"Sending email to {recipient_email}")
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info("Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
