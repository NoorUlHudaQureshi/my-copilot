import logging

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).with_name(".env"))

from livekit.agents import AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import silero, deepgram

from app.core.config import settings
from app.services.ollama_llm import OllamaLLM
from app.services.piper_tts import PiperTTS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")


async def entrypoint(ctx: JobContext):
    logger.info(f"Starting voice agent for room: {ctx.room.name}")

    vad = silero.VAD.load()

    stt = deepgram.STT(
        api_key=settings.DEEPGRAM_API_KEY
    )

    model = OllamaLLM()

    tts = PiperTTS(
        "en_US-lessac-medium.onnx"
    )

    session = AgentSession(
        vad=vad,
        stt=stt,
        llm=model,
        tts=tts,
    )

    await session.start(
        room=ctx.room,
    )

    await session.generate_reply(
        instructions="Say hello and ask how you can help."
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint)
    )