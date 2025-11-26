"""
API Testing Script for AI Document Chatbot
Run this after starting the backend server to test all endpoints
"""

import requests
import sys
import os

BASE_URL = "http://localhost:8000/api"

def test_complete_flow():
    """Test complete chatbot flow"""
    
    print("🧪 Starting API tests...\n")
    
    try:
        # 1. Create session
        print("1️⃣ Creating session...")
        response = requests.post(f"{BASE_URL}/session")
        assert response.status_code == 200, f"Failed to create session: {response.text}"
        session_id = response.json()["session_id"]
        print(f"✅ Session created: {session_id}\n")
        
        # 2. Check if sample file exists
        sample_file = "tests/samples/sample.pdf"
        if not os.path.exists(sample_file):
            print(f"⚠️  Sample file not found at {sample_file}")
            print("   Please create a tests/samples/ directory with a sample.pdf file")
            print("   Skipping upload test...\n")
        else:
            # 3. Upload document
            print("2️⃣ Uploading document...")
            with open(sample_file, "rb") as f:
                files = {"file": ("sample.pdf", f, "application/pdf")}
                response = requests.post(
                    f"{BASE_URL}/upload?session_id={session_id}",
                    files=files
                )
            assert response.status_code == 200, f"Failed to upload: {response.text}"
            print(f"✅ Document uploaded: {response.json()['chunks_created']} chunks\n")
            
            # 4. Get documents
            print("3️⃣ Getting documents...")
            response = requests.get(f"{BASE_URL}/documents?session_id={session_id}")
            assert response.status_code == 200, f"Failed to get documents: {response.text}"
            print(f"✅ Documents: {response.json()['total']}\n")
            
            # 5. Send chat message
            print("4️⃣ Sending chat message...")
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "query": "What is this document about?",
                    "session_id": session_id,
                    "language": "en"
                }
            )
            assert response.status_code == 200, f"Failed to chat: {response.text}"
            result = response.json()
            print(f"✅ Response: {result['response'][:100]}...")
            print(f"   Sources: {result['sources']}\n")
        
        # 6. Change language
        print("5️⃣ Changing language to Spanish...")
        response = requests.post(
            f"{BASE_URL}/session/{session_id}/language",
            json={"language": "es"}
        )
        assert response.status_code == 200, f"Failed to change language: {response.text}"
        print("✅ Language changed\n")
        
        # 7. Get session info
        print("6️⃣ Getting session info...")
        response = requests.get(f"{BASE_URL}/session/{session_id}")
        assert response.status_code == 200, f"Failed to get session: {response.text}"
        session_info = response.json()
        print(f"✅ Session info:")
        print(f"   Documents: {session_info['documents_count']}")
        print(f"   Messages: {session_info['messages_count']}")
        print(f"   Language: {session_info['language']}\n")
        
        print("🎉 All tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to backend server")
        print("   Make sure the backend is running at http://localhost:8000")
        return False
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    sys.exit(0 if success else 1)
