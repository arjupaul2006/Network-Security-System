import os 
import sys
from datetime import datetime

from Network_Security_System.constants import training_pipeline


print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        self.timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_name = training_pipeline.ARTIFACT_DIR
        self.artifacts_dir = os.path.join(self.artifacts_name, self.timestamp)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Artifacts/data_ingestion/
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifacts_name, training_pipeline.DATA_INGESTION_DIR_NAME)

        # Artifacts/data_ingestion/feature_store/phisingData.csv -> store raw data
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)

        # Artifacts/data_ingestion/train.csv -> store train data
        # Artifacts/data_ingestion/test.csv -> store test data
        self.train_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.TEST_FILE_NAME)

        self.train_test_spilt_ration: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.database_name: str = training_pipeline.DATA_INGESTIN_DATABASE_NAME
        self.collection_name: str = training_pipeline.DATA_INGESTIN_COLLECTION_NAME