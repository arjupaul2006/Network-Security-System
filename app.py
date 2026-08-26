import os
import sys
import pymongo
import pandas as pd

import certifi
ca = certifi.where()

from Network_Security_System.exception import CustomeException
from Network_Security_System.logger import logging

from Network_Security_System.constants.training_pipeline import DATA_INGESTIN_DATABASE_NAME, DATA_INGESTIN_COLLECTION_NAME

from Network_Security_System.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from Network_Security_System.utils.main_utils.utils import load_obj


from dotenv import load_dotenv
load_dotenv()
MONGODB_URL = os.getenv('MONGODB_URL')
print(MONGODB_URL)

client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
database = client[DATA_INGESTIN_DATABASE_NAME]
collection = database[DATA_INGESTIN_COLLECTION_NAME]


app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/', tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response('Training is successful')

    except Exception as e:
        raise CustomeException(e, sys)


if __name__ == '__main__':
    app_run(app, host='localhost', port=8000)