from Network_Security_System.exception import CustomeException
from Network_Security_System.logger import logging

import os
import sys

from Network_Security_System.entity.artifacts_entity import DataTransformationArtifacts, ModelTrainerArtifacts
from Network_Security_System.entity.config_entity import ModelTrainingConfig

from Network_Security_System.utils.ml_utils.metric.classification_metrix import get_classification_score
from Network_Security_System.utils.ml_utils.model.estimator import NetworkModel
from Network_Security_System.utils.main_utils.utils import save_object

from Network_Security_System.utils.main_utils.utils import load_numpy_array_data, load_obj, evalute_model

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier




class ModelTrainer:
    def __init__(self, data_transformation_artifacts: DataTransformationArtifacts, model_trainer_config: ModelTrainingConfig):
        try:
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_trainer_config = model_trainer_config

        except Exception as e:
            raise CustomeException(e, sys)


    def train_model(self,X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "AdaBoost Classifier": AdaBoostClassifier(), 
            "Gradient Boosting": GradientBoostingClassifier(verbose=1)
        }

        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost Classifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        model_report:dict = evalute_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, params=params)

        # get the best model
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        # get classification metrices
        classification_train_metric = get_classification_score(y_true=y_train,y_pred= y_train_pred)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        preprocessor = load_obj(file_path=self.data_transformation_artifacts.transformed_object_file_path)

        model_dir = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir, exist_ok=True)

        Network_model = NetworkModel(preprocessor=preprocessor, model=best_model) 
        save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=Network_model)

        model_trainer_artifacts = ModelTrainerArtifacts(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_matric_Artifacts=classification_train_metric,
            test_matric_Artifacts=classification_test_metric
        )
        logging.info(f'Train Model Artifacts: {model_trainer_artifacts}')
        return model_trainer_artifacts
        

    def initialte_model_trainer(self) -> ModelTrainerArtifacts:
        try:
            # load train and test array
            train_array_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_array_file_path = self.data_transformation_artifacts.transformed_test_file_path

            train_array = load_numpy_array_data(train_array_file_path)
            test_array = load_numpy_array_data(test_array_file_path)

            # divide the dependent and independent features
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_trainer_artifacts = self.train_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
            return model_trainer_artifacts

        except Exception as e:
            raise CustomeException(e, sys)