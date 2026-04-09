import numpy as np
import asyncio
from faster_whisper import WhisperModel

class Transcriber:
    def __init__(self):
        print("Loading Whisper Model... (This might take a moment)")
        self.model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
        print("Whisper Model Loaded!")

    def transcribe_audio(self, audio_bytes):
        """
        Converts raw audio bytes to text.
        """
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).flatten().astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(audio_array, beam_size=5)
        
        text = " ".join([segment.text for segment in segments]).strip()
        return text