import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL=os.getenv("MONGODB_URL")

import certifi
ca = certifi.where()


import numpy as np
import pandas as pd
import pymongo
from Network_Security_System.logger import logging
from Network_Security_System.exception import CustomeException

class NetworkSecurityPushData():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomeException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomeException(e, sys)

    def insert_to_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.records = self.collection.insert_many(self.records)
            return len(records)
        
        except Exception as e:
            raise CustomeException(e, sys)



if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = 'Network_Security'
    COLLECTION = 'raw_data'

    network_push_data_obj = NetworkSecurityPushData()
    RECORDS = network_push_data_obj.csv_to_json_converter(file_path=FILE_PATH)
    len_records = network_push_data_obj.insert_to_mongodb(records=RECORDS, database=DATABASE, collection=COLLECTION)
    print(len_records)

        

