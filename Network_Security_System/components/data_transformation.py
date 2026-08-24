from Network_Security_System.exception import CustomeException
from Network_Security_System.logger import logging

import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from Network_Security_System.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from Network_Security_System.entity.config_entity import DataTranformationConfig
from Network_Security_System.entity.artifacts_entity import DataValidationArtifacts, DataTransformationArtifacts
from Network_Security_System.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_transformation_config: DataTranformationConfig, data_validation_artifacts: DataValidationArtifacts):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomeException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomeException(e, sys)


    def get_transformed_object(self) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
         
        try:
            logging.info('Entered get_data_trnasformer_object method of Trnasformation class')

            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            preprocessor:Pipeline = Pipeline([('imputer', imputer)])
            return preprocessor


        except Exception as e:
            raise CustomeException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        try:
            # fetch the train and test data
            train_df = self.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifacts.valid_test_file_path)

            # separate the target column
            input_columns_train_df = train_df.drop(columns=TARGET_COLUMN)
            target_column_train_df = train_df[TARGET_COLUMN]
            target_column_train_df = target_column_train_df.replace(-1,0)

            input_columns_test_df = test_df.drop(columns=TARGET_COLUMN)
            target_column_test_df = test_df[TARGET_COLUMN]
            target_column_test_df = target_column_test_df.replace(-1,0)

            preprocessor = self.get_transformed_object()
            tranformed_train_df = preprocessor.fit_transform(input_columns_train_df)
            tranformed_test_df = preprocessor.transform(input_columns_test_df)

            train_arr = np.c_[tranformed_train_df, np.array(target_column_train_df)]
            test_arr = np.c_[tranformed_test_df, np.array(target_column_test_df)]

            # save the tranformed_train, tranformed_test, preprocessor to their particular file
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_obj_file_name, obj=preprocessor)

            data_transformation_artifacts = DataTransformationArtifacts(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_obj_file_name
            )

            return data_transformation_artifacts

        except Exception as e:
            raise CustomeException(e, sys)