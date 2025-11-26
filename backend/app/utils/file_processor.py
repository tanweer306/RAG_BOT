import magic
from typing import Optional

class FileProcessor:
    @staticmethod
    def validate_file_type(file_content: bytes, filename: str) -> bool:
        """Validate file type using python-magic"""
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(file_content)
            
            allowed_types = {
                'application/pdf': ['.pdf'],
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
                'text/plain': ['.txt'],
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
                'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx']
            }
            
            file_extension = '.' + filename.split('.')[-1].lower()
            
            for mime_type, extensions in allowed_types.items():
                if file_type.startswith(mime_type.split('/')[0]) and file_extension in extensions:
                    return True
            
            return False
        except Exception as e:
            # Fallback to extension checking
            allowed_extensions = ['.pdf', '.docx', '.txt', '.xlsx', '.pptx']
            return any(filename.lower().endswith(ext) for ext in allowed_extensions)
