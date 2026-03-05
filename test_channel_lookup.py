"""Test YouTube channel lookup - Troubleshooting script"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from googleapiclient.discovery import build

print("=" * 60)
print("YouTube Channel Lookup Test")
print("=" * 60)
print()

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=Config.YOUTUBE_API_KEY)

channel_username = Config.YOUTUBE_CHANNEL_USERNAME.lstrip("@")
print(f"Looking for channel: @{channel_username}")
print()

# Method 1: Search by name
print("Method 1: Searching by channel name...")
try:
    request = youtube.search().list(
        part="snippet",
        q=channel_username,
        type="channel",
        maxResults=10
    )
    response = request.execute()
    
    if response.get("items"):
        print(f"Found {len(response['items'])} channels:")
        for idx, item in enumerate(response["items"]):
            channel_id = item["snippet"]["channelId"]
            title = item["snippet"]["title"]
            description = item["snippet"]["description"][:100] if item["snippet"]["description"] else "No description"
            print(f"\n{idx+1}. Channel: {title}")
            print(f"   ID: {channel_id}")
            print(f"   Description: {description}...")
            
            # Get subscriber count
            try:
                channel_details = youtube.channels().list(
                    part="statistics",
                    id=channel_id
                ).execute()
                if channel_details.get("items"):
                    subs = channel_details["items"][0]["statistics"].get("subscriberCount", "Hidden")
                    videos = channel_details["items"][0]["statistics"].get("videoCount", "0")
                    print(f"   Subscribers: {subs}")
                    print(f"   Videos: {videos}")
            except:
                pass
    else:
        print("No channels found!")
except Exception as e:
    print(f"Error: {e}")

print()
print("=" * 60)
print()

# Method 2: Direct channel URL lookup
print("TIP: If you know the channel URL, you can extract the channel ID:")
print("1. Go to the channel page on YouTube")
print("2. Look at the URL:")
print("   - If it's like: youtube.com/channel/UCxxxxx")
print("     The channel ID is: UCxxxxx")
print("   - If it's like: youtube.com/@username")
print("     Right-click the page → View Page Source")
print("     Search for 'channelId' to find the ID")
print()
print("Then update your .env file to use the Channel ID directly:")
print("  YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxx")
print()

print("=" * 60)
print()

# Ask user which one to use
print("Which channel is correct? (Enter the number, or 0 to cancel)")
choice = input("Choice: ").strip()

if choice.isdigit() and int(choice) > 0:
    idx = int(choice) - 1
    try:
        request = youtube.search().list(
            part="snippet",
            q=channel_username,
            type="channel",
            maxResults=10
        )
        response = request.execute()
        
        if idx < len(response["items"]):
            selected_channel_id = response["items"][idx]["snippet"]["channelId"]
            selected_title = response["items"][idx]["snippet"]["title"]
            
            print()
            print(f"Selected: {selected_title}")
            print(f"Channel ID: {selected_channel_id}")
            print()
            
            # Get uploads playlist
            channel_details = youtube.channels().list(
                part="contentDetails",
                id=selected_channel_id
            ).execute()
            
            if channel_details.get("items"):
                uploads_playlist = channel_details["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                print(f"Uploads Playlist ID: {uploads_playlist}")
                
                # Test getting videos
                print()
                print("Testing video retrieval...")
                playlist_items = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=uploads_playlist,
                    maxResults=5
                ).execute()
                
                if playlist_items.get("items"):
                    print(f"✓ Found {len(playlist_items['items'])} recent videos:")
                    for item in playlist_items["items"]:
                        print(f"  - {item['snippet']['title']}")
                    print()
                    print("SUCCESS! This channel works correctly.")
                    print()
                    print("To use this channel, add to your .env file:")
                    print(f"YOUTUBE_CHANNEL_ID={selected_channel_id}")
                else:
                    print("⚠ No videos found for this channel")
            
    except Exception as e:
        print(f"Error: {e}")

print()
print("Test complete!")
