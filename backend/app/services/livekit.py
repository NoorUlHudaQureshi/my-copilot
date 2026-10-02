from livekit import api
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger("ai-copilot")

class LiveKitService:
    def __init__(self):
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        self.url = settings.LIVEKIT_URL

    async def create_token(self, room_name: str, identity: str) -> Optional[str]:
        """
        Generates a real LiveKit access token.
        """
        if not self.api_key or not self.api_secret:
            logger.error("LiveKit API credentials are not configured in .env")
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
            logger.error(f"LiveKit Token Error: {e}")
            return None

livekit_service = LiveKitService()
