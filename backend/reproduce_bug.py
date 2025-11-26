from app.utils.text_chunker import TextChunker
import sys

def test_chunker_fix():
    print("🧪 Testing TextChunker Fix...")
    
    # Create a text that triggers the bug:
    # Short sentence + very long sentence
    chunk_size = 1000
    overlap = 200
    text = "Hi. " + "a" * 2000
    
    print(f"Text length: {len(text)}")
    
    try:
        chunks = TextChunker.chunk_text(text, chunk_size, overlap)
        print(f"✅ Success! Generated {len(chunks)} chunks.")
        print("First chunk:", chunks[0][:20] + "...")
        if len(chunks) > 1:
            print("Second chunk:", chunks[1][:20] + "...")
    except MemoryError:
        print("❌ FAILED: MemoryError (Infinite Loop)")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_chunker_fix()
