from Network_Security_System.logger import logging
from Network_Security_System.exception import CustomeException

from Network_Security_System.entity.config_entity import DataValidationConfig
from Network_Security_System.entity.artifacts_entity import DataValidationArtifacts, DataIngestionArtifacts
from Network_Security_System.constants.training_pipeline import SCHEME_FILE_NAME
from Network_Security_System.utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

class DataValidation:
    def __init__(self, data_ingestion_artifacts: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self._scheme_config = read_yaml_file(SCHEME_FILE_NAME)

        except Exception as e:
            raise CustomeException(e, sys)


    @staticmethod
    def read_file(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomeException(e, sys)


    def validate_number_of_columns(self, df: pd.DataFrame):
        try:
            number_of_col_in_scheme = len(self._scheme_config)

            logging.info(f'Required number of columns: {number_of_col_in_scheme}')
            logging.info(f'The col of the dataframe: {df.columns}')

            # compare the number of columns
            if len(df.columns) == number_of_col_in_scheme:
                return True
            return False

        except Exception as e:
            raise CustomeException(e, sys)


    def validate_numerical_col(self, df: pd.DataFrame):
        try:
            number_of_numerical_col = len(self._scheme_config['numerical_columns'])
            number_of_numerical_col_in_df = len(df.select_dtypes(exclude='str').columns)

            logging.info(f'Required number of numerical col: {number_of_numerical_col}')
            logging.info(f'Number of numerical col in datafram: {number_of_numerical_col_in_df}')

            if number_of_numerical_col_in_df == number_of_numerical_col:
                return True
            return False

        except Exception as e:
            raise CustomeException(e, sys)

    def detect_data_drift(self, base_df, current_df, thresold=0.05) -> bool:
        try:
            status=True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if thresold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status=False

                report.update({column: {
                    'p_value': float(is_same_dist.pvalue),
                    'drift_status': is_found
                }})

            # write the report into drift yaml file
            drift_report_file_path = self.data_validation_config.drift_report_file
            dir_name = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status

        except Exception as e:
            raise CustomeException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            train_data_file_path = self.data_ingestion_artifacts.trained_file_path
            test_data_file_path = self.data_ingestion_artifacts.tested_file_path

            # read the train and test data
            train_df = self.read_file(train_data_file_path)
            test_df = self.read_file(test_data_file_path)


            # validate the number of columns
            status = self.validate_number_of_columns(df=train_df)
            if not status:
                error_msg = f'Train data does not contain all columns\n'

            status = self.validate_number_of_columns(df=test_df)
            if not status:
                error_msg = f'Test data does not contain all columns\n'


            # validate the number numerical columns
            status = self.validate_numerical_col(df=train_df)
            if not status:
                error_msg = f'Train data does not contain all numerical columns\n'

            status = self.validate_numerical_col(df=test_df)
            if not status:
                error_msg = f'Test data does not contain all numerical columns\n'


            # let check draft
            status = self.detect_data_drift(base_df=train_df, current_df=test_df)
            if status:
                dir_name = os.path.dirname(self.data_validation_config.valid_test_file)
                os.makedirs(dir_name, exist_ok=True)

                train_df.to_csv(self.data_validation_config.valid_train_file, index=False, header=True)
                test_df.to_csv(self.data_validation_config.valid_test_file, index=False, header=True)

                data_validation_artifacts = DataValidationArtifacts(
                    validation_status=status,
                    valid_train_file_path=self.data_validation_config.valid_train_file,
                    valid_test_file_path=self.data_validation_config.valid_test_file,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file
                )
                return data_validation_artifacts


        except Exception as e:
            raise CustomeException(e, sys)

    