import os
import sys
import numpy as np

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

""" Data Transformation Related Constant """

DATA_TRANSFORMATION_DIR_NAME:str = 'data_trainsformation'
DATA_TRANSFORMATION_TRANFORMED_DATA_DIR:str = 'transformed_data'
DATA_TRANSFORMATION_TRANFORMED_OBJECT_DIR:str = 'trasformed_object'
DATA_TRANSFORMATION_TRANFORMED_OBJECT_FILE_NAME:str = 'preprocessing.pkl'

# KNN Imputer to replace the nan value
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    'missing_values': np.nan,
    'n_neighbors': 3,
    'weights': 'uniform',
} 

""" Model Training Related Constant """

MODEL_TRAINER_DIR_NAME:str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME:str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05