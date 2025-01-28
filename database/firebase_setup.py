import firebase_admin
import os
import json
import base64
from firebase_admin import credentials
from dotenv import load_dotenv

print("FIREBASE_SERVICE_ACCOUNT:", os.getenv("FIREBASE_SERVICE_ACCOUNT"))
# Load environment variables
load_dotenv(override=False)

# Get the Base64-encoded service account string from the environment variable
firebase_creds_base64 = os.getenv("FIREBASE_SERVICE_ACCOUNT2")
if not firebase_creds_base64:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable is not set")

# Decode the Base64-encoded string
firebase_creds_json = base64.b64decode(firebase_creds_base64).decode("utf-8")
print(firebase_creds_json)

# Parse the JSON
FIREBASE_SERVICE_ACCOUNT = json.loads(firebase_creds_json)

# Initialize Firebase Admin SDK
def init_firebase_admin():
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })

# Call the initialization function
init_firebase_admin()
