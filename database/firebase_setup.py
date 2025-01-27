import firebase_admin
import os
import json
from firebase_admin import credentials
import streamlit as st
from dotenv import load_dotenv

# Load .env file locally (this will work when running locally)
if not os.getenv('CI'):  # Check if not running in CI (e.g., GitHub Actions)
    load_dotenv()

# Access the Firebase credentials from Streamlit Secrets (for Streamlit Cloud)
if 'CI' in os.environ:  # If running in Streamlit Cloud, use st.secrets
    firebase_creds = st.secrets["FIREBASE_SERVICE_ACCOUNT"]
else:  # If running locally, get it from the .env file
    firebase_creds = os.getenv("FIREBASE_SERVICE_ACCOUNT")

# Ensure the Firebase credentials are available
if not firebase_creds:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT secret is not set")

# Parse the Firebase credentials JSON
FIREBASE_SERVICE_ACCOUNT = json.loads(firebase_creds)

def init_firebase_admin():
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })
