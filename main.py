from database import firebase_setup,firebase_database
# test read and write to database
firebase_setup.init_firebase_admin()
test_data = {"test_key": "test_value"}
firebase_database.write_to_database(test_data, "/test_path")
data = firebase_database.read_from_database("/test_path")
print(data)