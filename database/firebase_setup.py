import firebase_admin
from firebase_admin import credentials

def init_firebase_admin():
    cred = credentials.Certificate("./database/firebase_config.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://realestate-data-collector-default-rtdb.firebaseio.com/"
    })
