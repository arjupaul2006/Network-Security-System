from Network_Security_System.exception import CustomeException
from Network_Security_System.logger import logging
import sys

# this is for prediction of new data
class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise CustomeException(e, sys)

    def predict(self, x):
        try:
            x_tranformed = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_tranformed)
            return y_pred

        except Exception as e:
            raise CustomeException(e, sys)