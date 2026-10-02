import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.plugins import openai, silero, deepgram
from app.services.llm import llm_service
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")

async def entrypoint(ctx: JobContext):
    logger.info(f"Starting voice agent for room: {ctx.room.name}")

    # Initialize the voice pipeline
    # 1. VAD (Voice Activity Detection) - Silero is great for local use
    vad = silero.VAD.load()

    # 2. STT (Speech-to-Text) - Deepgram is fast and industry standard
    # Note: Requires DEEPGRAM_API_KEY in .env
    stt = deepgram.STT()

    # 3. LLM - Using our existing logic via a wrapper
    # For LiveKit agents, we typically use their LLM interface
    model = openai.LLM(model="gpt-4o-mini")

    # 4. TTS (Text-to-Speech) - OpenAI TTS is high quality
    tts = openai.TTS()

    # Create the agent
    agent = llm.VoiceAssistant(
        vad=vad,
        stt=stt,
        llm=model,
        tts=tts,
        chat_ctx=llm.ChatContext().append(
            role="system",
            text="You are a helpful AI Assistant. Keep your responses concise and friendly for voice interaction."
        ),
    )

    # Start the agent in the room
    agent.start(ctx.room)

    # Keep the agent alive
    await agent.say("Hello! I am your AI Assistant. How can I help you today?")

if __name__ == "__main__":
    # This allows us to run the agent using: python voice_agent.py dev
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
