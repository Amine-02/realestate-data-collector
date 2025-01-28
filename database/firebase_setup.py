import firebase_admin
from firebase_admin import credentials
import streamlit as st

# Get Firebase credentials from Streamlit secrets
FIREBASE_SERVICE_ACCOUNT = st.secrets["FIREBASE_SERVICE_ACCOUNT"]

def init_firebase_admin():
    # Initialize Firebase Admin SDK with credentials from secrets
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })
