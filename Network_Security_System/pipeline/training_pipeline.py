import os
import sys

from Network_Security_System.exception import CustomeException
from Network_Security_System.logger import logging

from Network_Security_System.components.data_ingestion import DataIngestion
from Network_Security_System.components.data_validation import DataValidation
from Network_Security_System.components.data_transformation import DataTransformation
from Network_Security_System.components.model_training import ModelTrainer

from Network_Security_System.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTranformationConfig,
    ModelTrainingConfig 
)

from Network_Security_System.entity.artifacts_entity import (
    DataIngestionArtifacts, 
    DataValidationArtifacts, 
    DataTransformationArtifacts,
    ModelTrainerArtifacts
)



class TrainingPipeline:
    def __init__(self):
        self.training_pipeline = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline)

            logging.info('Start Data Ingestion')
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifacts = self.data_ingestion.initiate_data_ingestion()
            logging.info(f'Data Ingestion Completed and Artifacts: {self.data_ingestion_artifacts}')

            return self.data_ingestion_artifacts

        except Exception as e:
            raise CustomeException(e, sys)

    def start_data_validation(self):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline)

            logging.info('Start Data Validation')
            self.data_validation = DataValidation(
                data_ingestion_artifacts=self.data_ingestion_artifacts, 
                data_validation_config=self.data_validation_config
            )
            self.data_validation_artifacts = self.data_validation.initiate_data_validation()
            logging.info(f'DataValidation Completed and Artifacts: {self.data_ingestion_artifacts}')

            return self.data_validation_artifacts

        except Exception as e:
            raise CustomeException(e, sys)

    def start_data_transformation(self):
        try:
            self.data_transformation_config = DataTranformationConfig(training_pipeline_config=self.training_pipeline)

            logging.info('Start Data Transformation')
            self.data_transformation = DataTransformation(
                data_validation_artifacts=self.data_validation_artifacts,
                data_transformation_config=self.data_transformation_config
            )
            self.data_transformation_artifacts = self.data_transformation.initiate_data_transformation()
            logging.info(f'Data Transformation Completed and Artifacts: {self.data_transformation_artifacts}')

        except Exception as e:
            raise CustomeException(e, sys)

    def start_model_trainer(self):
        try:
            self.model_trainer_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline)

            logging.info('Start Model Training')
            self.model_trainer = ModelTrainer(
                data_transformation_artifacts=self.data_transformation_artifacts,
                model_trainer_config=self.model_trainer_config
            )
            self.model_trainer_artifacts = self.model_trainer.initialte_model_trainer()
            logging.info(f'Model Training completed and Artifacts: {self.model_trainer_artifacts}')

            return self.model_trainer_artifacts

        except Exception as e:
            raise CustomeException(e, sys)

    def run_pipeline(self):
        try: 
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation()
            data_transformation_artifact = self.start_data_transformation()
            model_trainer_artifact = self.start_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise CustomeException(e, sys)