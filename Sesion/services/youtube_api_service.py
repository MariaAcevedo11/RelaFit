import requests
import os
from dotenv import load_dotenv
from .video_service_interface import IVideoService

load_dotenv()

class YouTubeAPIService(IVideoService):

    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")

    def get_video_data(self, video_id: str):
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet",
            "id": video_id,
            "key": self.api_key
        }

        response = requests.get(url, params=params).json()

        if "items" not in response or not response["items"]:
            return None
        
        return response["items"][0]
