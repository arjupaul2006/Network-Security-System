from Network_Security_System.exception import CustomeException

from Network_Security_System.entity.artifacts_entity import ClassificationMatricArtifacts
from sklearn.metrics import f1_score, precision_score, recall_score

import sys

def get_classification_score(y_true, y_pred) -> ClassificationMatricArtifacts:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)

        classification_matrics_artifacts = ClassificationMatricArtifacts(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )

        return classification_matrics_artifacts

    except Exception as e:
        raise CustomeException(e,sys)