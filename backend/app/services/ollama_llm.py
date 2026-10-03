import uuid
import httpx

from livekit.agents import llm
from livekit.agents.types import (
    APIConnectOptions,
    DEFAULT_API_CONNECT_OPTIONS,
    NOT_GIVEN,
    NotGivenOr,
)

from app.core.config import settings


class OllamaLLMStream(llm.LLMStream):
    async def _run(self) -> None:
        messages = []

        for message in self.chat_ctx.messages():
            text = message.text_content or ""
            if text:
                messages.append({
                    "role": message.role,
                    "content": text,
                })

        payload = {
            "model": self._llm.model,
            "messages": messages,
            "stream": True,
        }

        request_id = str(uuid.uuid4())

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{settings.OLLAMA_BASE_URL}/api/chat",
                json=payload,
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    data = __import__("json").loads(line)
                    content = data.get("message", {}).get("content", "")

                    if content:
                        await self._event_ch.send(
                            llm.ChatChunk(
                                id=request_id,
                                delta=llm.ChoiceDelta(
                                    role="assistant",
                                    content=content,
                                ),
                            )
                        )

                    if data.get("done"):
                        break


class OllamaLLM(llm.LLM):
    def __init__(self):
        super().__init__()

    @property
    def model(self) -> str:
        return settings.DEFAULT_MODEL

    @property
    def provider(self) -> str:
        return "ollama"

    def chat(
        self,
        *,
        chat_ctx: llm.ChatContext,
        tools=None,
        conn_options: APIConnectOptions = DEFAULT_API_CONNECT_OPTIONS,
        parallel_tool_calls: NotGivenOr[bool] = NOT_GIVEN,
        tool_choice=NOT_GIVEN,
        extra_kwargs: NotGivenOr[dict] = NOT_GIVEN,
    ) -> llm.LLMStream:
        return OllamaLLMStream(
            llm=self,
            chat_ctx=chat_ctx,
            tools=tools or [],
            conn_options=conn_options,
        )