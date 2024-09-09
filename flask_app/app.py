from flask import Flask, render_template,request
import mlflow
from preprocessing_utility import normalize_text
import dagshub
import pickle
import pandas as pd
import json
import os
from mlflow.tracking import MlflowClient
# dagshub.init(repo_owner='NaumanRafique12', repo_name='mini-mlops-Project', mlflow=True)
# mlflow.set_tracking_uri('https://dagshub.com/NaumanRafique12/mini-mlops-Project.mlflow')
# dagshub.init(repo_owner='noman.rafique', repo_name='new_mini_mlops_emotion', mlflow=True)

# mlflow.set_tracking_uri('https://dagshub.com/noman.rafique/new_mini_mlops_emotion.mlflow')
import os
from dotenv import load_dotenv

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
# mlflow.set_tracking_uri("https://dagshub.com/noman.rafique/mini-mlops-Project-ci.mlflow")
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
app = Flask(__name__)

# # load model from model registry
def get_latest_model_version(model_name):
    client = MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_version:
        latest_version = client.get_latest_versions(model_name, stages=["None"])
    return latest_version[0].version if latest_version else None

model_name = "my_model"

# # Step 1: Read the JSON file
# json_file_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'versions.json')
# # Reading the JSON file
# with open(json_file_path, "r") as f:
#     data = json.load(f)
# run_id = data.get(str(get_latest_model_version(model_name)))
run_id = "6b549b63b4a240ac8dfbd9bd72fa1513"
# logged_model = 'runs:/9d2ae11f5f9a42bfa47e12cebd10eab7/Logistic Regression'
logged_model = f'runs:/{run_id}/Logistic Regression'

# Load model as a PyFuncModel.
model = mlflow.pyfunc.load_model(logged_model)
# Step 2: Get the value of 'V1' (assuming it contains the dataset path)

vectorizer = pickle.load(open('models/vectorizer.pkl','rb'))
# model = pickle.load(open(r"C:\Users\VU360solutions\Desktop\mlops\mini-mlops-project\models\model.pkl",'rb'))


@app.route('/')
def home():
    return render_template('index.html',result=None)

@app.route('/predict', methods=['POST'])
def predict():

    text = request.form['text']

    # clean
    text = normalize_text(text)
    
    features = vectorizer.transform([text])  # Vectorize the text
 

# Generate column names dynamically based on the number of columns in the features
    num_columns = features.shape[1]
    column_names = [str(i) for i in range(num_columns)]
    data = pd.DataFrame(features.toarray(),columns=column_names)
    result = model.predict(data)
    
    

    # show
    return render_template('index.html', result= result[0])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")