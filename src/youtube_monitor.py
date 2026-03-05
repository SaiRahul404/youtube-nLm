"""YouTube channel monitoring module."""

import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import safe_str

logger = logging.getLogger(__name__)


class YouTubeMonitor:
    """Monitor YouTube channel for new video uploads."""
    
    def __init__(self, api_key: str, channel_username: str = None, channel_id: str = None):
        """
        Initialize YouTube monitor.
        
        Args:
            api_key: YouTube Data API v3 key
            channel_username: YouTube channel username (e.g., @MoneyPurse) - optional if channel_id provided
            channel_id: YouTube channel ID (e.g., UCxxxxx) - optional if channel_username provided
        """
        self.api_key = api_key
        self.channel_username = channel_username.lstrip("@") if channel_username else None
        self.channel_id = channel_id
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self._uploads_playlist_id = None
    
    def get_channel_id(self) -> Optional[str]:
        """
        Get the channel ID from channel username.
        
        Returns:
            Channel ID or None if not found
        """
        try:
            # First try with forHandle (for @username format)
            logger.info(f"Looking up channel: @{self.channel_username}")
            request = self.youtube.channels().list(
                part="id,snippet,contentDetails",
                forHandle=self.channel_username
            )
            response = request.execute()
            
            if response.get("items"):
                channel_id = response["items"][0]["id"]
                channel_title = response["items"][0]["snippet"]["title"]
                logger.info(f"Found channel: {safe_str(channel_title)} (ID: {channel_id})")
                return channel_id
            
            # Try with forUsername (legacy username format)
            logger.info(f"Trying legacy username lookup...")
            request = self.youtube.channels().list(
                part="id,snippet,contentDetails",
                forUsername=self.channel_username
            )
            response = request.execute()
            
            if response.get("items"):
                channel_id = response["items"][0]["id"]
                channel_title = response["items"][0]["snippet"]["title"]
                logger.info(f"Found channel: {safe_str(channel_title)} (ID: {channel_id})")
                return channel_id
            
            # Last resort: search by name
            logger.info(f"Trying search by name...")
            request = self.youtube.search().list(
                part="snippet",
                q=self.channel_username,
                type="channel",
                maxResults=5
            )
            response = request.execute()
            
            if response.get("items"):
                # Log all found channels for user to verify
                logger.info(f"Search found {len(response['items'])} channels:")
                for idx, item in enumerate(response["items"]):
                    logger.info(f"  {idx+1}. {safe_str(item['snippet']['title'])} (ID: {item['snippet']['channelId']})")
                
                # Use the first match
                channel_id = response["items"][0]["snippet"]["channelId"]
                channel_title = response["items"][0]["snippet"]["title"]
                logger.warning(f"Using first match: {safe_str(channel_title)} (ID: {channel_id})")
                logger.warning(f"If this is wrong, try using the channel ID directly in your config")
                return channel_id
            
            logger.error(f"Channel @{self.channel_username} not found via any method")
            return None
            
        except HttpError as e:
            logger.error(f"HTTP error getting channel ID: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting channel ID: {e}")
            return None
    
    def get_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        """
        Get the uploads playlist ID for a channel.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Uploads playlist ID or None if error
        """
        if self._uploads_playlist_id:
            return self._uploads_playlist_id
        
        try:
            logger.info(f"Getting uploads playlist for channel: {channel_id}")
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            if response.get("items"):
                self._uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                logger.info(f"Found uploads playlist ID: {self._uploads_playlist_id}")
                return self._uploads_playlist_id
            
            logger.error(f"No uploads playlist found for channel {channel_id}")
            logger.error(f"The channel might not exist or might not have any videos")
            return None
            
        except HttpError as e:
            logger.error(f"HTTP error getting uploads playlist: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting uploads playlist: {e}")
            return None
    
    def check_for_new_videos(self, uploads_playlist_id: str, max_results: int = 5) -> List[Dict]:
        """
        Check for new videos in the uploads playlist.
        
        Args:
            uploads_playlist_id: YouTube uploads playlist ID
            max_results: Maximum number of recent videos to check (default: 5)
            
        Returns:
            List of video dictionaries with id, title, publishedAt, and url
        """
        try:
            request = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=max_results
            )
            response = request.execute()
            
            videos = []
            for item in response.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_data = {
                    "id": video_id,
                    "title": item["snippet"]["title"],
                    "publishedAt": item["snippet"]["publishedAt"],
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                }
                videos.append(video_data)
            
            logger.info(f"Found {len(videos)} recent videos")
            return videos
            
        except HttpError as e:
            logger.error(f"HTTP error checking for videos: {e}")
            return []
        except Exception as e:
            logger.error(f"Error checking for videos: {e}")
            return []
    
    def get_latest_videos(self, max_results: int = 5) -> List[Dict]:
        """
        Get the latest videos from the monitored channel.
        
        Args:
            max_results: Maximum number of recent videos to retrieve
            
        Returns:
            List of video dictionaries
        """
        # Get channel ID (use provided ID or look it up)
        if self.channel_id:
            logger.info(f"Using provided channel ID: {self.channel_id}")
            channel_id = self.channel_id
        else:
            channel_id = self.get_channel_id()
            if not channel_id:
                logger.error("Could not get channel ID")
                return []
        
        # Get uploads playlist ID
        uploads_playlist_id = self.get_uploads_playlist_id(channel_id)
        if not uploads_playlist_id:
            logger.error("Could not get uploads playlist ID")
            return []
        
        # Check for new videos
        return self.check_for_new_videos(uploads_playlist_id, max_results)
