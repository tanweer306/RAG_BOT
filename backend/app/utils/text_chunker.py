from typing import List

class TextChunker:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if not text:
            return []
            
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            
            # Try to break at sentence end if we haven't reached the end of text
            if end < text_len:
                best_end = -1
                found_valid_delimiter = False
                
                # Look for sentence endings
                for delimiter in ['. ', '! ', '? ', '\n\n']:
                    last_delimiter = text[start:end].rfind(delimiter)
                    
                    if last_delimiter != -1:
                        potential_end = start + last_delimiter + len(delimiter)
                        
                        # CRITICAL FIX: Only accept delimiters that allow us to advance
                        # beyond the overlap region. Otherwise we get stuck or go backwards.
                        if potential_end > start + overlap:
                            if potential_end > best_end:
                                best_end = potential_end
                                found_valid_delimiter = True
                
                # If we found a valid delimiter that respects overlap, use it
                if found_valid_delimiter:
                    end = best_end
            
            # Clamp end to text length
            end = min(end, text_len)
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Prepare for next iteration
            if end >= text_len:
                break
                
            # Calculate next start position
            next_start = end - overlap
            
            # SAFETY: Ensure we always advance at least 1 character
            if next_start <= start:
                next_start = start + 1
            
            start = next_start
        
        return chunks
