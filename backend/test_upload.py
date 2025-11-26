import requests
import os

BASE_URL = "http://localhost:8000/api"

def test_upload():
    # 1. Create a dummy file
    filename = "test_doc.txt"
    with open(filename, "w") as f:
        f.write("This is a test document for the RAG chatbot. It contains some sample text to verify the upload and embedding process.")
    
    try:
        # 2. Create session
        print("Creating session...")
        try:
            response = requests.post(f"{BASE_URL}/session")
            if response.status_code != 200:
                print(f"❌ Session creation failed: {response.status_code} - {response.text}")
                return
            session_id = response.json()["session_id"]
            print(f"✅ Session created: {session_id}")
        except requests.exceptions.ConnectionError:
             print(f"❌ Could not connect to {BASE_URL}. Is the backend running?")
             return

        # 3. Upload document
        print(f"Uploading {filename}...")
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "text/plain")}
            response = requests.post(f"{BASE_URL}/upload?session_id={session_id}", files=files)
            
        if response.status_code == 200:
            print(f"✅ Document uploaded successfully!")
            print(response.json())
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"Response: {response.text}")

    finally:
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_upload()
