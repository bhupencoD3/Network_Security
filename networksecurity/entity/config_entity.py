from networksecurity.constant import training_pipeline
import os
from datetime import datetime
from networksecurity.logging.logger import (
    logging,
)  # Using custom logger for uniform logs

# Print basic pipeline constants for quick CLI feedback
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:
    """
    Training Pipeline Configuration Class

    Handles creation of the main artifact directory with a unique timestamp.
    This is the root directory under which all other artifacts will be stored.
    """

    def __init__(self, timestamp=datetime.now()):
        try:
            # Store pipeline name from constants
            self.pipeline_name = training_pipeline.PIPELINE_NAME

            # Format timestamp for directory naming
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Base directory name for storing artifacts
            self.artifact_name = training_pipeline.ARTIFACT_DIR

            # Final artifact path: e.g., "artifact/2025-05-11_15-32-45"
            self.artifact_dir = os.path.join(self.artifact_name, str(timestamp))

            # Store the final timestamp used
            self.timestamp = timestamp

            logging.info("✅ TrainingPipelineConfig initialized.")
            logging.info(f"Pipeline Name: {self.pipeline_name}")
            logging.info(f"Artifact Directory Path: {self.artifact_dir}")
        except Exception as e:
            logging.error("❌ Failed to initialize TrainingPipelineConfig.")
            raise e


class DataIngestionConfig:
    """
    Data Ingestion Configuration Class

    Handles paths and constants needed for data ingestion like:
    - Feature store CSV location
    - Train/Test split paths
    - Collection and database info for MongoDB
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            # Main ingestion directory inside artifact directory
            self.data_ingestion_dir = os.path.join(
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_INGESTION_DIR_NAME,
            )

            # Feature store file (raw processed dataset)
            self.feature_store_file_path = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            )

            # Paths for train and test CSVs after splitting
            self.training_file_path = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TRAIN_FILE_NAME,
            )

            self.test_file_path = os.path.join(
                self.data_ingestion_dir,
                training_pipeline.DATA_INGESTION_INGESTED_DIR,
                training_pipeline.TEST_FILE_NAME,
            )

            # Ratio for train/test split (from constants)
            self.train_test_split_ratio = (
                training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            )

            # MongoDB collection and database names
            self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME

            logging.info("✅ DataIngestionConfig initialized successfully.")
            logging.info(f"Data Ingestion Directory: {self.data_ingestion_dir}")
            logging.info(f"Feature Store File Path: {self.feature_store_file_path}")
            logging.info(f"Training File Path: {self.training_file_path}")
            logging.info(f"Testing File Path: {self.test_file_path}")
            logging.info(f"MongoDB Database: {self.database_name}")
            logging.info(f"MongoDB Collection: {self.collection_name}")
        except Exception as e:
            logging.error("❌ Failed to initialize DataIngestionConfig.")
            raise e
