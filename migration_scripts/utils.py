from google.cloud import firestore
from google.oauth2 import service_account

def initialize_firestore(key_file_path="./firebase-test-env.json"):
    """Initializes a Firestore client with credentials from a key file."""
    try:
        credentials = service_account.Credentials.from_service_account_file(key_file_path)
        db = firestore.Client(credentials=credentials)
        return db
    except Exception as e:
        print(f"Error initializing Firestore: {e}")
        return None