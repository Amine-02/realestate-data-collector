import firebase_admin
import os
import json
from firebase_admin import credentials

firebase_creds = os.getenv("FIREBASE_SERVICE_ACCOUNT")
if not firebase_creds:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable is not set")
FIREBASE_SERVICE_ACCOUNT = json.loads(firebase_creds)
def init_firebase_admin():
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })
