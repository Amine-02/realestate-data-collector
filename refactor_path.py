from script.site_scraper import ALL_BOROUGHS
from database import firebase_setup, firebase_database

def init_database():
    # Initialize Firebase Admin once at the start
    firebase_setup.init_firebase_admin()

def move_multiple_paths_to_apartments(old_paths):
    for old_path in old_paths:
        # 1) Read data from the old path
        data = firebase_database.read_from_database(old_path)
        
        if data is None:
            print(f"No data found at path '{old_path}'; skipping.")
            continue
        
        new_path = f"apartments/{old_path}"
        firebase_database.append_to_database(data, new_path)
        print(f"Data from '{old_path}' successfully copied to '{new_path}'.")


if __name__ == "__main__":
    init_database()
    move_multiple_paths_to_apartments(ALL_BOROUGHS)