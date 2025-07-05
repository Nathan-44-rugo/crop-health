# test_api.py
import requests
import os

# --- CONFIGURATION ---
# The full URL to your running FastAPI endpoint
API_URL = "http://192.168.187.245:8000/diagnose"
# The path to an image you want to test
IMAGE_PATH = "./early.JPG" # <--- CHANGE THIS

# Check if the image file exists
if not os.path.exists(IMAGE_PATH):
    print(f"Error: Image not found at {IMAGE_PATH}")
else:
    # Open the image file in binary read mode
    with open(IMAGE_PATH, 'rb') as f:
        files = {'file': (os.path.basename(IMAGE_PATH), f, 'image/jpeg')}
        
        try:
            print(f"Sending request to {API_URL}...")
            response = requests.post(API_URL, files=files)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            # Print the result
            print("\n✅ Success! Server Response:")
            print(response.json())

        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error connecting to the API: {e}")