from datetime import date
from dataclasses import asdict

from database import firebase_setup, firebase_database
from script import realtor_scraper

def update_stats_for_borough(borough: str):
    # Initialize Firebase Admin once at the start
    firebase_setup.init_firebase_admin()

    # Compute statistics and convert to dict
    stats_dict = asdict(realtor_scraper.compute_stats(borough))
    
    # Get today's date as a string
    today_date = date.today().isoformat()  # "YYYY-MM-DD"
    
    # Path in your database where city stats are stored
    db_path = f"/{borough}"
    
    # Read existing data (if any)
    existing_data = firebase_database.read_from_database(db_path) or {}
    
    # Check if today's date already exists
    if any(entry.get("date") == today_date for entry in existing_data.values()):
        print(f"Entry for {today_date} already exists. Skipping write.")
    else:
        # Write new data to the database
        firebase_database.append_to_database(stats_dict, db_path)
        print(f"New entry for {today_date} added.")

if __name__ == "__main__":
    update_stats_for_borough("saint-hubert")
