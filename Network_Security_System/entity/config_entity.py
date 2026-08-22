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
        # Artifacts/timestamp/data_ingestion/
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifacts_dir, training_pipeline.DATA_INGESTION_DIR_NAME)

        # Artifacts/timestamp/data_ingestion/feature_store/phisingData.csv -> store raw data
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)

        # Artifacts/timestamp/data_ingestion/train.csv -> store train data
        # Artifacts/timestamp/data_ingestion/test.csv -> store test data
        self.train_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.TEST_FILE_NAME)

        self.train_test_spilt_ration: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.database_name: str = training_pipeline.DATA_INGESTIN_DATABASE_NAME
        self.collection_name: str = training_pipeline.DATA_INGESTIN_COLLECTION_NAME

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # Artifacts/timestamp/data_validation/
        self.data_validation_dir = os.path.join(training_pipeline_config.artifacts_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)

        # Artifacts/timestamp/data_validation/validated/ -> Valid Data
        # Artifacts/timestamp/data_validation/invalidated -> Invalid Data
        self.valid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)

        # Artifacts/timestamp/data_validation/validated/train.csv
        # Artifacts/timestamp/data_validation/validated/test.csv
        self.valid_train_file = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)

        # Artifacts/timestamp/data_validation/invalidated/train.csv
        # Artifacts/timestamp/data_validation/invalidated/test.csv
        self.invalid_train_file = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)

        # Artifacts/timestamp/data_validation/drift_report_report.yaml
        self.drift_report_file = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )