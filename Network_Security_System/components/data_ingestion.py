import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split

from Network_Security_System.exception import CustomeException
from Network_Security_System.logger import logging

from dotenv import load_dotenv
load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')

# configuration of data ingestion cofig
from Network_Security_System.entity.config_entity import DataIngestionConfig
from Network_Security_System.entity.artifacts_entity import DataIngestionArtifacts



class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomeException(e,sys)

    def fetch_the_raw_data_from_mongodb_as_df(self):
        """ Fetch the data from mongodb """
        try:
            self.database = self.data_ingestion_config.database_name
            self.collection = self.data_ingestion_config.collection_name

            mongo_client = pymongo.MongoClient(MONGODB_URL)
            collection = mongo_client[self.database][self.collection]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns="_id", inplace=True)

            df.replace('na', np.nan, inplace=True)

            return df

        except Exception as e:
            raise CustomeException(e, sys)


    def export_dataframe_to_csv(self, df: pd.DataFrame):
       try:
        feature_file_path = self.data_ingestion_config.feature_store_file_path
        dir_name = os.path.dirname(feature_file_path)
        os.makedirs(dir_name, exist_ok=True)
        df.to_csv(feature_file_path, index=False, header=True)
        return df

       except Exception as e:
           raise CustomeException(e, sys)
    

    def train_test_split(self, df: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                df, 
                test_size=self.data_ingestion_config.train_test_spilt_ration
            )
            logging.info('Train Test Split Done')

            dir_name = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_name, exist_ok=True)
            logging.info('Created the folder to store the train and test dataset')

            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info('Exporting the train test dataset into particular file')
            return df
        except Exception as e:
            raise CustomeException(e, sys)

    def initiate_data_ingestion(self):
        try:
            df = self.fetch_the_raw_data_from_mongodb_as_df()
            df = self.export_dataframe_to_csv(df=df)
            df = self.train_test_split(df=df)

            data_ingestion_artifacts = DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.train_file_path, tested_file_path=self.data_ingestion_config.test_file_path)
            return data_ingestion_artifacts

        except Exception as e:
            raise CustomeException(e, sys)