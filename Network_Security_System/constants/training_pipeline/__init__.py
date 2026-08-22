import os
import sys

""" Data Ingestion related Constant """

DATA_INGESTIN_DATABASE_NAME:str = 'Network_Security'
DATA_INGESTIN_COLLECTION_NAME:str = 'raw_data'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2

TARGET_COLUMN:str = 'Result'
PIPELINE_NAME:str = 'NetworkSecurity'
ARTIFACT_DIR:str = 'Artifacts'
FILE_NAME:str = 'phisingData.csv'

TRAIN_FILE_NAME:str = 'train.csv'
TEST_FILE_NAME:str = 'test.csv'
SCHEME_FILE_NAME = os.path.join('data_scheme', 'scheme.yaml')

""" Data Validation related Constant """

DATA_VALIDATION_DIR_NAME:str = 'data_validation'
DATA_VALIDATION_VALID_DIR:str = 'validated'
DATA_VALIDATION_INVALID_DIR:str = 'invalidated'
DATA_VALIDATION_DRIFT_REPORT_DIR:str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = 'report.yaml'