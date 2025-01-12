from firebase_admin import db

def write_to_database(data, path="/"):
        ref = db.reference(path)
        ref.set(data)

def append_to_database(data, path="/"):
        ref = db.reference(path)
        ref.push(data)

def read_from_database(path="/"):
        ref = db.reference(path)
        data = ref.get()
        return data

def remove_from_database(path="/"):
        ref = db.reference(path)
        ref.delete()