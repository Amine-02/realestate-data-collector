import firebase_admin
import os
import json
from firebase_admin import credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
firebase_creds = os.getenv("FIREBASE")
if not firebase_creds:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT:", print(os.getenv("FIREBASE")))

# Parse the JSON
FIREBASE = json.loads(firebase_creds)

# Initialize Firebase Admin SDK
def init_firebase_admin():
    cred = credentials.Certificate(FIREBASE)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })