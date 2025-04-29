import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Extract DB credentials from .env
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Validate environment variables
if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError("❌ Missing one or more required MongoDB environment variables.")

# Construct MongoDB URI
MONGO_URI = (
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
    f"/?retryWrites=true&w=majority&appName={DB_NAME}"
)


def test_mongo_connection(uri: str):
    """
    Ping MongoDB to verify connection is successful.
    """
    try:
        client = MongoClient(uri)
        client.admin.command("ping")
        print("✅ Successfully connected to MongoDB and pinged the server.")
    except Exception as e:
        print(f"🔥 Failed to connect to MongoDB: {e}")
    finally:
        client.close()
        print("🔒 MongoDB connection closed.")


if __name__ == "__main__":
    test_mongo_connection(MONGO_URI)
