from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class TranslationService:
    LANGUAGE_NAMES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ar": "Arabic",
        "ur": "Urdu",
        "zh": "Chinese (Simplified)"
    }
    
    @staticmethod
    async def translate_text(text: str, target_language: str) -> str:
        """Translate text to target language"""
        if target_language == "en":
            return text  # Already in English
        
        language_name = TranslationService.LANGUAGE_NAMES.get(target_language, "English")
        
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following text to {language_name}. Maintain the original meaning and tone."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
