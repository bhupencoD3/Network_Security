import os
import sys
import json
import certifi
import pymongo
import pandas as pd
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException

# Load environment variables
load_dotenv()

# MongoDB credentials from .env
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Validate credentials
if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError("Missing required environment variables.")

# Construct MongoDB URI
MONGO_URI = (
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
    f"/?retryWrites=true&w=majority&appName={DB_NAME}"
)

# TLS certificate path
CA_FILE = certifi.where()

# File path to CSV
FILE_PATH = os.path.join("Network_Data", "phishingData.csv")

# MongoDB target database and collection
DATABASE = "network_security"
COLLECTION_NAME = "phishing_data"


class NetworkDataExtract:
    def __init__(self):
        # No setup needed at init for now
        pass

    def csv_to_json(self, file_path: str):
        """
        Convert a CSV file to a list of JSON records.
        """
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data(self, records: list, db_name: str, collection_name: str):
        """
        Insert records into MongoDB collection.
        """
        try:
            client = pymongo.MongoClient(MONGO_URI, tlsCAFile=CA_FILE)
            db = client[db_name]
            collection = db[collection_name]

            result = collection.insert_many(records)
            print(
                f"✅ Inserted {len(result.inserted_ids)} records into '{collection_name}'."
            )

            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        finally:
            client.close()
            print("🔒 MongoDB connection closed.")


if __name__ == "__main__":
    try:
        extractor = NetworkDataExtract()

        print(f"📄 Reading data from: {FILE_PATH}")
        records = extractor.csv_to_json(FILE_PATH)

        print(f"🚀 Inserting into MongoDB: {DB_NAME}.{COLLECTION_NAME}")
        inserted_count = extractor.insert_data(records, DATABASE, COLLECTION_NAME)

        print(f"🎉 Successfully inserted {inserted_count} records.")

    except NetworkSecurityException as ne:
        print(f"🔥 Custom Exception: {ne}")
    except Exception as ex:
        print(f"❌ Unexpected Error: {ex}")
