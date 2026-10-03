import asyncio
from pathlib import Path

from livekit import rtc
from livekit.agents import APIConnectOptions, tts
from livekit.agents.tts import AudioEmitter
from piper.voice import PiperVoice


class PiperTTSStream(tts.ChunkedStream):
    async def _run(self, output_emitter: AudioEmitter) -> None:
        voice = self._tts.voice

        chunks = await asyncio.to_thread(
            lambda: list(voice.synthesize(self._input_text))
        )

        for chunk in chunks:
            audio_bytes = chunk._audio_int16_bytes

            if not audio_bytes:
                audio_bytes = chunk._audio_int16_bytes

            frame = rtc.AudioFrame(
                data=audio_bytes,
                sample_rate=chunk.sample_rate,
                num_channels=chunk.sample_channels,
                samples_per_channel=len(audio_bytes) // (
                    chunk.sample_width * chunk.sample_channels
                ),
            )

            output_emitter.push(frame.data)


class PiperTTS(tts.TTS):
    def __init__(self, model_path: str):
        super().__init__(
            capabilities=tts.TTSCapabilities(
                streaming=False,
                aligned_transcript=False,
            ),
            sample_rate=22050,
            num_channels=1,
        )

        self.voice = PiperVoice.load(Path(model_path))
        self._label = "piper"
        self._model = "en_US-lessac-medium"
        self._provider = "piper"

    @property
    def model(self):
        return self._model

    @property
    def provider(self):
        return self._provider

    def synthesize(
        self,
        text: str,
        *,
        conn_options: APIConnectOptions = APIConnectOptions(),
    ) -> tts.ChunkedStream:
        return PiperTTSStream(
            tts=self,
            input_text=text,
            conn_options=conn_options,
        )