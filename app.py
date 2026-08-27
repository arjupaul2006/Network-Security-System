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
from Network_Security_System.utils.ml_utils.model.estimator import NetworkModel
from form_data import FormData
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Form
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

# import the HTML File
from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='./templates')

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



@app.post('/predict')
async def predict(request: Request, file:UploadFile = File(...)):
    try:
        preprocessor = load_obj('final_model/preprocessor.pkl')
        model = load_obj('final_model/model.pkl')

        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        df = pd.read_csv('valid_data/test.csv')
        y_pred = network_model.predict(df)
        df['Predicted_output'] = y_pred

        df.to_csv('predicted_output/output.csv')
        table_html = df.to_html(classes='table table-striped')

        return template.TemplateResponse(
            request=request,
            name="table.html",
            context={"table": table_html}
        )

    except Exception as e:
        raise CustomeException(e, sys)


@app.get('/form')
async def form_page(request: Request):
    try:
        return template.TemplateResponse(
            request=request,
            name='form.html',
            context={}
        )

    except Exception as e:
        raise CustomeException(e, sys)


@app.post('/form')
async def form_prediction(
    request: Request,
    form_data: Annotated[FormData, Form()]
):
    try:
        print(form_data)

        preprocessor = load_obj('final_model/preprocessor.pkl')
        model = load_obj('final_model/model.pkl')
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        df = pd.DataFrame([form_data.model_dump()])
        prediction = network_model.predict(df)

        prediction = -1.0 if prediction == 0.0 else 1.0

        print('Predicted result: ', prediction)

        return template.TemplateResponse(
            request=request,
            name='form.html',
            context={'result': prediction}
        )

    except Exception as e:
        raise CustomeException(e, sys)


if __name__ == '__main__':
    app_run(app, host='localhost', port=8000)