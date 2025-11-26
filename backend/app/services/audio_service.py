from openai import AsyncOpenAI
from app.config import settings
import base64
from pathlib import Path

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class AudioService:
    @staticmethod
    async def transcribe_audio(audio_file_path: str) -> str:
        """Transcribe audio to text using Whisper"""
        with open(audio_file_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model=settings.OPENAI_WHISPER_MODEL,
                file=audio_file
            )
        return transcript.text
    
    @staticmethod
    async def text_to_speech(text: str, language: str = "en") -> bytes:
        """Convert text to speech using OpenAI TTS"""
        
        # Map language codes to voice names
        voice_map = {
            "en": "alloy",
            "es": "nova",
            "fr": "shimmer",
            "de": "onyx",
            "ar": "fable",
            "ur": "echo",
            "zh": "nova"
        }
        
        voice = voice_map.get(language, "alloy")
        
        response = await client.audio.speech.create(
            model=settings.OPENAI_TTS_MODEL,
            voice=voice,
            input=text
        )
        
        return response.content
