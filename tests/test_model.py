# load test + signature test + performance test

import unittest
import mlflow
import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Retrieve the token
dagshub_token = os.getenv('DAGSHUB_PAT')

if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "noman.rafique"
repo_name = "mini-mlops-Project-ci"
# mlflow.set_tracking_uri("https://dagshub.com/noman.rafique/mini-mlops-Project-ci.mlflow")
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
import os
import json
import mlflow
from mlflow.tracking import MlflowClient

def load_latest_model(json_file_relative_path=os.path.join('..', 'reports', 'versions.json'), model_name="my_model"):
    def get_latest_model_version(model_name):
        client = MlflowClient()
        latest_version = client.get_latest_versions(model_name, stages=["Staging"])
        if not latest_version:
            latest_version = client.get_latest_versions(model_name, stages=["None"])
        return latest_version[0].version if latest_version else None

    # Step 1: Read the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), json_file_relative_path)
    
    # Reading the JSON file
    with open(json_file_path, "r") as f:
        data = json.load(f)
    
    # Get the latest run_id using the model name
    run_id = data.get(str(get_latest_model_version(model_name)))
    
    # Construct the logged model path
    logged_model = f'runs:/{run_id}/Logistic Regression'

    # Load model as a PyFuncModel
    model = mlflow.pyfunc.load_model(logged_model)
    return model

class TestModelLoading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up DagsHub credentials for MLflow tracking
        cls.holdout_data = pd.read_csv(os.path.join(os.path.dirname(__file__),'..', 'data', 'features','test_tfidf.csv'))

# Retrieve the token
        dagshub_token = os.getenv('DAGSHUB_TOKEN')

        if not dagshub_token:
            raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

        os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

        dagshub_url = "https://dagshub.com"
        repo_owner = "noman.rafique"
        repo_name = "mini-mlops-Project-ci"
        # mlflow.set_tracking_uri("https://dagshub.com/noman.rafique/mini-mlops-Project-ci.mlflow")
        mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

       
        # Load the new model from MLflow model registry
        cls.new_model_name = "my_model"
        cls.new_model_version = cls.get_latest_model_version(cls.new_model_name)
        cls.new_model = load_latest_model()

        # Load the vectorizer
        cls.vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))
        
        # Load holdout test data

    @staticmethod
    def get_latest_model_version(model_name, stage="Staging"):
        client = mlflow.MlflowClient()
        latest_version = client.get_latest_versions(model_name, stages=[stage])
        return latest_version[0].version if latest_version else None

    def test_model_loaded_properly(self):
        self.assertIsNotNone(self.new_model)

    def test_model_signature(self):
        # Create a dummy input for the model based on expected input shape
        input_text = "hi how are you"
        input_data = self.vectorizer.transform([input_text])
        input_df = pd.DataFrame(input_data.toarray(), columns=[str(i) for i in range(input_data.shape[1])])

        # Predict using the new model to verify the input and output shapes
        prediction = self.new_model.predict(input_df)
       
        # Verify the input shape
        self.assertEqual(input_df.shape[1], len(self.vectorizer.get_feature_names_out()))

        # Verify the output shape (assuming binary classification with a single output)
        self.assertEqual(len(prediction), input_df.shape[0])
        self.assertEqual(len(prediction.shape), 1)  # Assuming a single output column for binary classification

    def test_model_performance(self):
        # Extract features and labels from holdout test data
        X_holdout = self.holdout_data.iloc[:,0:-1]
        y_holdout = self.holdout_data.iloc[:,-1]

        # Predict using the new model
        y_pred_new = self.new_model.predict(X_holdout)

        # Calculate performance metrics for the new model
        accuracy_new = accuracy_score(y_holdout, y_pred_new)
        precision_new = precision_score(y_holdout, y_pred_new)
        recall_new = recall_score(y_holdout, y_pred_new)
        f1_new = f1_score(y_holdout, y_pred_new)

        # Define expected thresholds for the performance metrics
        expected_accuracy = 0.02
        expected_precision = 0.02
        expected_recall = 0.02
        expected_f1 = 0.02

        # Assert that the new model meets the performance thresholds
        self.assertGreaterEqual(accuracy_new, expected_accuracy, f'Accuracy should be at least {expected_accuracy}')
        self.assertGreaterEqual(precision_new, expected_precision, f'Precision should be at least {expected_precision}')
        self.assertGreaterEqual(recall_new, expected_recall, f'Recall should be at least {expected_recall}')
        self.assertGreaterEqual(f1_new, expected_f1, f'F1 score should be at least {expected_f1}')

if __name__ == "__main__":
    unittest.main()