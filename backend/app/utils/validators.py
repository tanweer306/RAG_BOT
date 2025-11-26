from typing import Optional
import re

class Validators:
    @staticmethod
    def validate_session_id(session_id: str) -> bool:
        """Validate session ID format (UUID)"""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(session_id))
    
    @staticmethod
    def validate_language_code(language: str) -> bool:
        """Validate language code"""
        allowed_languages = ['en', 'es', 'fr', 'de', 'ar', 'ur', 'zh']
        return language in allowed_languages
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove any path components
        filename = filename.split('/')[-1].split('\\')[-1]
        # Remove any dangerous characters
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
        return filename
