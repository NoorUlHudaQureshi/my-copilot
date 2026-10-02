from livekit import api
from app.core.config import settings
from typing import Optional

class LiveKitService:
    def __init__(self):
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        self.url = settings.LIVEKIT_URL

    async def create_token(self, room_name: str, identity: str) -> Optional[str]:
        """
        Generates a LiveKit access token for a client to join a room.
        """
        if not self.api_key or not self.api_secret:
            print("LiveKit API credentials are not configured.")
            return None

        try:
            token = api.AccessToken(self.api_key, self.api_secret) \
                .with_identity(identity) \
                .with_grants(api.VideoGrants(
                    room_join=True,
                    room=room_name,
                ))
            return token.to_jwt()
        except Exception as e:
            print(f"LiveKit Token Error: {e}")
            return None

livekit_service = LiveKitService()
