import edge_tts
import os
import asyncio

class Synthesizer:
    def __init__(self):
        self.voice = "en-US-AriaNeural"

    async def speak(self, text):
        """
        Converts text to an MP3 file and returns the filename.
        """
        filename = "response.mp3"
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(filename)
        
        return filename