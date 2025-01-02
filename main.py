from datetime import date
from dataclasses import asdict
from script.constants import ALL_BOROUGHS

from database import firebase_setup, firebase_database
from script import realtor_scraper

def init_database():
    # Initialize Firebase Admin once at the start
    firebase_setup.init_firebase_admin()

def update_stats_for_borough(borough: str):
    # Compute statistics and convert to dict
    stats_dict = asdict(realtor_scraper.compute_stats(borough))
    
    # Get today's date as a string
    today_date = date.today().isoformat()  # "YYYY-MM-DD"
    
    # Path in your database where city stats are stored
    db_path = f"/{borough}"
    
    # Fetch existing data under the borough path
    existing_data = firebase_database.read_from_database(db_path) or {}

    # Check if today's date already exists in any entry
    entry_exists = any(entry.get("date") == today_date for entry in existing_data.values())

    if entry_exists:
        print(f"Entry for {today_date} in borough '{borough}' already exists. Skipping write.")
    else:
        # Add the new data (append as a new entry)
        firebase_database.append_to_database(stats_dict, db_path)
        print(f"New entry for {today_date} in borough '{borough}' added.")

if __name__ == "__main__":
    init_database()
    for borough in ALL_BOROUGHS:
        update_stats_for_borough(borough)

