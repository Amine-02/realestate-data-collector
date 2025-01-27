import firebase_admin
import os
import json
from firebase_admin import credentials
from dotenv import load_dotenv

# Only load .env file in local development, not in CI environments
if not os.getenv('CI'):  # Check if not running in CI (e.g., GitHub Actions)
    load_dotenv()

# Get the Firebase credentials from the environment
firebase_creds = os.getenv("FIREBASE_SERVICE_ACCOUNT")

# Ensure the environment variable is set
if not firebase_creds:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable is not set")

# Parse the Firebase credentials JSON
FIREBASE_SERVICE_ACCOUNT = json.loads(firebase_creds)

def init_firebase_admin():
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })
