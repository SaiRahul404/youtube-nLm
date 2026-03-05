"""State management module for tracking processed videos."""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from filelock import FileLock

logger = logging.getLogger(__name__)


class StateManager:
    """Manage state for processed videos."""
    
    def __init__(self, state_file_path: str):
        """
        Initialize state manager.
        
        Args:
            state_file_path: Path to the JSON state file
        """
        self.state_file_path = Path(state_file_path)
        self.lock_file_path = Path(str(self.state_file_path) + ".lock")
        self.state_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize state file if it doesn't exist
        if not self.state_file_path.exists():
            self._initialize_state_file()
    
    def _initialize_state_file(self):
        """Initialize an empty state file."""
        initial_state = {
            "processed_videos": [],
            "last_check": None,
            "channel_uploads_playlist_id": None
        }
        with FileLock(self.lock_file_path):
            with open(self.state_file_path, "w") as f:
                json.dump(initial_state, f, indent=2)
        logger.info(f"Initialized state file at {self.state_file_path}")
    
    def load_state(self) -> Dict:
        """
        Load state from file.
        
        Returns:
            Dictionary containing state data
        """
        try:
            with FileLock(self.lock_file_path):
                with open(self.state_file_path, "r") as f:
                    state = json.load(f)
                return state
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding state file: {e}")
            logger.info("Creating backup and initializing new state file")
            self._backup_corrupted_state()
            self._initialize_state_file()
            return self.load_state()
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            raise
    
    def save_state(self, state: Dict):
        """
        Save state to file.
        
        Args:
            state: Dictionary containing state data
        """
        try:
            with FileLock(self.lock_file_path):
                with open(self.state_file_path, "w") as f:
                    json.dump(state, f, indent=2)
            logger.debug("State saved successfully")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            raise
    
    def _backup_corrupted_state(self):
        """Create a backup of corrupted state file."""
        if self.state_file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.state_file_path.parent / f"processed_videos_backup_{timestamp}.json"
            try:
                self.state_file_path.rename(backup_path)
                logger.info(f"Backed up corrupted state to {backup_path}")
            except Exception as e:
                logger.error(f"Error backing up corrupted state: {e}")
    
    def is_processed(self, video_id: str) -> bool:
        """
        Check if a video has been processed.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if video has been processed, False otherwise
        """
        state = self.load_state()
        processed_ids = [v["video_id"] for v in state["processed_videos"]]
        return video_id in processed_ids
    
    def mark_processed(
        self,
        video_id: str,
        title: str,
        published_at: str,
        notebook_id: str,
        status: str = "success"
    ):
        """
        Mark a video as processed.
        
        Args:
            video_id: YouTube video ID
            title: Video title
            published_at: Video publish timestamp
            notebook_id: NotebookLM notebook ID
            status: Processing status (success, error, etc.)
        """
        state = self.load_state()
        
        # Check if already exists
        existing = next(
            (v for v in state["processed_videos"] if v["video_id"] == video_id),
            None
        )
        
        if existing:
            logger.warning(f"Video {video_id} already marked as processed")
            # Update status if changed
            existing["status"] = status
            existing["processed_at"] = datetime.now().isoformat()
        else:
            # Add new entry
            video_entry = {
                "video_id": video_id,
                "title": title,
                "published_at": published_at,
                "processed_at": datetime.now().isoformat(),
                "notebook_id": notebook_id,
                "status": status
            }
            state["processed_videos"].append(video_entry)
            logger.info(f"Marked video {video_id} as processed with status: {status}")
        
        self.save_state(state)
    
    def get_processed_videos(self) -> List[Dict]:
        """
        Get list of all processed videos.
        
        Returns:
            List of processed video dictionaries
        """
        state = self.load_state()
        return state["processed_videos"]
    
    def update_last_check(self):
        """Update the last check timestamp."""
        state = self.load_state()
        state["last_check"] = datetime.now().isoformat()
        self.save_state(state)
        logger.debug("Updated last check timestamp")
    
    def get_uploads_playlist_id(self) -> Optional[str]:
        """
        Get cached uploads playlist ID.
        
        Returns:
            Uploads playlist ID or None
        """
        state = self.load_state()
        return state.get("channel_uploads_playlist_id")
    
    def set_uploads_playlist_id(self, playlist_id: str):
        """
        Cache uploads playlist ID.
        
        Args:
            playlist_id: YouTube uploads playlist ID
        """
        state = self.load_state()
        state["channel_uploads_playlist_id"] = playlist_id
        self.save_state(state)
        logger.info(f"Cached uploads playlist ID: {playlist_id}")
