import dagshub
import mlflow
import os
# dagshub.init(repo_owner='noman.rafique', repo_name='mini-mlops-Project-ci', mlflow=True)
# # # Fetch username and token from environment variables
# os.environ['MLFLOW_TRACKING_USERNAME'] = 'noman.rafique'
# os.environ['MLFLOW_TRACKING_PASSWORD'] = '123'
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the token
dagshub_token = os.getenv('DAGSHUB_TOKEN')

if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "noman.rafique"
repo_name = "mini-mlops-Project-ci"

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

# mlflow.set_tracking_uri("https://dagshub.com/noman.rafique/mini-mlops-Project-ci.mlflow")
with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)