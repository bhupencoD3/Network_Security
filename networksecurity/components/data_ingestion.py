import os
import sys
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from sklearn.model_selection import train_test_split

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataIngestionConfig

# Load environment variables from .env
load_dotenv()

# Fetch MongoDB credentials from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Ensure all required environment variables are set
if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError("❌ Missing one or more required MongoDB environment variables.")

# Construct MongoDB URI dynamically
MONGO_URI = (
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
    f"/?retryWrites=true&w=majority&appName={DB_NAME}"
)


class DataIngestion:
    """
    Handles the end-to-end data ingestion process:
    - Exporting data from MongoDB
    - Saving it to a local feature store
    - Splitting into train/test sets
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info("📦 DataIngestion instance initialized with provided config.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Connect to MongoDB and export the specified collection as a DataFrame.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(
                f"📡 Connecting to MongoDB: {DB_HOST} | DB: {database_name} | Collection: {collection_name}"
            )
            self.mongo_client = MongoClient(MONGO_URI)

            collection = self.mongo_client[database_name][collection_name]
            data = collection.find()
            df = pd.DataFrame(list(data))

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
                logging.info("🗑️ Dropped '_id' column from DataFrame.")

            df.replace({"na": np.nan}, inplace=True)
            logging.info(f"📋 Retrieved {len(df)} records from MongoDB.")

            self.mongo_client.close()
            logging.info("🔌 MongoDB connection closed.")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_feature_store(self, df: pd.DataFrame):
        """
        Export the raw data to the feature store directory.
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            directory = os.path.dirname(feature_store_path)

            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"📁 Created feature store directory at: {directory}")

            df.to_csv(feature_store_path, index=False, header=True)
            logging.info(f"✅ Exported data to feature store at: {feature_store_path}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, df: pd.DataFrame):
        """
        Split the raw data into train and test sets and save them to CSVs.
        """
        try:
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42,
            )

            logging.info(
                f"✂️ Split data into Train: {train_set.shape}, Test: {test_set.shape}"
            )

            directory = os.path.dirname(self.data_ingestion_config.training_file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(
                    f"📂 Created directory for train/test sets at: {directory}"
                )

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False)

            logging.info(
                f"📁 Training data saved at: {self.data_ingestion_config.training_file_path}"
            )
            logging.info(
                f"📁 Testing data saved at: {self.data_ingestion_config.test_file_path}"
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """
        Complete the data ingestion pipeline:
        1. Read data from MongoDB
        2. Save raw data
        3. Perform train-test split
        4. Return the ingestion artifact
        """
        try:
            logging.info("🚀 Starting data ingestion process...")

            df = self.export_collection_as_dataframe()
            if df.empty:
                raise ValueError(
                    "❌ DataFrame is empty. No data retrieved from MongoDB."
                )

            logging.info("✅ DataFrame loaded. Proceeding with export and split...")
            df = self.export_data_feature_store(df)
            self.split_data_as_train_test(df)

            artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )
            logging.info("🎯 Data ingestion completed and artifact created.")
            return artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
