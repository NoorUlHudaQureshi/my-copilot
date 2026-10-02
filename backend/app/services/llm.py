import httpx
import json
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.core.config import settings
from app.agents.registry import registry

class LLMProvider:
    def __init__(self):
        self.ollama_url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        self.default_model = settings.DEFAULT_MODEL

    async def generate_chat_response(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False
    ) -> Any:
        """
        Generate a response using Ollama. Now supports Tool calling if the model allows.
        """
        # Add tools to the payload if the model supports it
        tools = registry.get_all_metadata()

        payload = {
            "model": self.default_model,
            "messages": messages,
            "stream": stream,
            "tools": tools if tools else None
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                if not stream:
                    response = await client.post(self.ollama_url, json=payload)
                    response.raise_for_status()

                    result = response.json().get("message", {})
                    # Handle tool calls
                    if "tool_calls" in result and result["tool_calls"]:
                        return {"type": "tool_call", "tool_calls": result["tool_calls"]}

                    return {"type": "text", "content": result.get("content", "")}

                async with client.stream("POST", self.ollama_url, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            chunk = json.loads(line)
                            if "message" in chunk:
                                yield chunk["message"].get("content", "")
                            if chunk.get("done"):
                                break
        except Exception as e:
            print(f"Ollama Error: {e}")
            return {"type": "error", "content": "I'm having trouble connecting to my brain right now."}

llm_service = LLMProvider()
