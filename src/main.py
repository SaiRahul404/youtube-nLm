"""Main orchestration script for YouTube NotebookLM automation."""

import sys
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from youtube_monitor import YouTubeMonitor
from state_manager import StateManager
from notebooklm_handler import NotebookLMHandler
from email_sender import EmailSender
from utils import safe_str


def setup_logging():
    """Configure logging for the application."""
    # Ensure log directory exists
    Config.LOG_DIR.mkdir(exist_ok=True)
    
    # Create handlers with UTF-8 encoding
    file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Console handler with error handling for Unicode
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Set formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("YouTube NotebookLM Automation Started")
    logger.info("=" * 60)
    return logger


def main():
    """Main orchestration function."""
    logger = setup_logging()
    
    try:
        # Validate configuration
        logger.info("Validating configuration...")
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Initialize components
        logger.info("Initializing components...")
        youtube_monitor = YouTubeMonitor(
            Config.YOUTUBE_API_KEY,
            channel_username=Config.YOUTUBE_CHANNEL_USERNAME,
            channel_id=Config.YOUTUBE_CHANNEL_ID
        )
        
        state_manager = StateManager(Config.STATE_FILE_PATH)
        
        notebooklm_handler = NotebookLMHandler(Config.NOTEBOOKLM_NOTEBOOK_ID)
        
        email_sender = EmailSender(
            Config.EMAIL_SMTP_SERVER,
            Config.EMAIL_SMTP_PORT,
            Config.EMAIL_SENDER,
            Config.EMAIL_PASSWORD
        )
        logger.info("All components initialized successfully")
        
        # Check for new videos
        logger.info(f"Checking for new videos from {Config.YOUTUBE_CHANNEL_USERNAME}...")
        videos = youtube_monitor.get_latest_videos(max_results=1)
        
        if not videos:
            logger.warning("No videos found. Check channel configuration.")
            state_manager.update_last_check()
            return
        
        logger.info(f"Found {len(videos)} recent videos")
        
        # Filter for unprocessed videos
        new_videos = [v for v in videos if not state_manager.is_processed(v["id"])]
        
        if not new_videos:
            logger.info("No new videos to process")
            state_manager.update_last_check()
            return
        
        logger.info(f"Found {len(new_videos)} new videos to process")
        
        # Process each new video
        for video in new_videos:
            video_id = video["id"]
            video_title = video["title"]
            video_url = video["url"]
            published_at = video["publishedAt"]
            
            logger.info("=" * 60)
            logger.info(f"Processing video: {safe_str(video_title)}")
            logger.info(f"URL: {video_url}")
            logger.info("=" * 60)
            
            try:
                # Process video through NotebookLM
                logger.info("Processing video through NotebookLM...")
                analysis = notebooklm_handler.process_video(
                    video_url,
                    Config.NOTEBOOKLM_PROMPT
                )
                
                if not analysis:
                    logger.error("Failed to get analysis from NotebookLM")
                    # Mark as error to avoid retry loops
                    state_manager.mark_processed(
                        video_id,
                        video_title,
                        published_at,
                        Config.NOTEBOOKLM_NOTEBOOK_ID,
                        status="error"
                    )
                    continue
                
                logger.info(f"Received analysis ({len(analysis)} characters)")
                
                # Send email notification
                logger.info("Sending email notification...")
                email_success = email_sender.send_video_analysis(
                    Config.EMAIL_RECIPIENT,
                    video_title,
                    video_url,
                    analysis
                )
                
                if not email_success:
                    logger.warning("Failed to send email, but marking video as processed")
                
                # Mark as processed
                state_manager.mark_processed(
                    video_id,
                    video_title,
                    published_at,
                    Config.NOTEBOOKLM_NOTEBOOK_ID,
                    status="success"
                )
                
                logger.info(f"Successfully processed video: {safe_str(video_title)}")
                
            except Exception as e:
                logger.error(f"Error processing video {video_id}: {e}")
                # Mark as error to avoid retry loops
                state_manager.mark_processed(
                    video_id,
                    video_title,
                    published_at,
                    Config.NOTEBOOKLM_NOTEBOOK_ID,
                    status="error"
                )
                continue
        
        # Update last check timestamp
        state_manager.update_last_check()
        
        logger.info("=" * 60)
        logger.info("Processing complete")
        logger.info("=" * 60)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
