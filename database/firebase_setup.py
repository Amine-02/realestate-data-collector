import firebase_admin
import os
import json
import base64
from firebase_admin import credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
firebase_creds_base64 = os.getenv("FIREBASE_BASE64")

if not firebase_creds_base64:
    raise ValueError("Environment variable FIREBASE_BASE64 is missing or not set.")

firebase_creds = json.loads(base64.b64decode(firebase_creds_base64).decode('utf-8'))
print(firebase_creds)

# Initialize Firebase Admin SDK
def init_firebase_admin():
    # Check if Firebase is already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
        })
    else:
        print("Firebase already initialized.")
