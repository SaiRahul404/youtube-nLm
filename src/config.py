"""Configuration management for YouTube NotebookLM automation."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # YouTube API Configuration
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_CHANNEL_USERNAME = os.getenv("YOUTUBE_CHANNEL_USERNAME", "@MoneyPurse")
    YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")  # Optional: use channel ID directly
    
    # NotebookLM Configuration
    NOTEBOOKLM_NOTEBOOK_ID = os.getenv("NOTEBOOKLM_NOTEBOOK_ID")
    
    # Email Configuration
    EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "465"))
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
    
    # NotebookLM Prompt
    NOTEBOOKLM_PROMPT = os.getenv(
        "NOTEBOOKLM_PROMPT",
        "Analyze this video and provide key insights, takeaways, and actionable recommendations."
    )
    
    # State File Configuration
    STATE_FILE_PATH = os.getenv(
        "STATE_FILE_PATH",
        str(Path.home() / ".youtube_notebooklm" / "processed_videos.json")
    )
    
    # Logging Configuration
    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "automation.log"
    
    @classmethod
    def validate(cls):
        """Validate required configuration values."""
        required_fields = [
            ("YOUTUBE_API_KEY", cls.YOUTUBE_API_KEY),
            ("NOTEBOOKLM_NOTEBOOK_ID", cls.NOTEBOOKLM_NOTEBOOK_ID),
            ("EMAIL_SENDER", cls.EMAIL_SENDER),
            ("EMAIL_PASSWORD", cls.EMAIL_PASSWORD),
            ("EMAIL_RECIPIENT", cls.EMAIL_RECIPIENT),
        ]
        
        missing = [field for field, value in required_fields if not value]
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}. "
                f"Please check your .env file."
            )
        
        return True


# Validate configuration on import
if __name__ != "__main__":
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
