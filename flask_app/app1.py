# import pickle
# import pandas as pd 
# import json
# from flask import Flask, render_template,request
# import mlflow
# from preprocessing_utility import normalize_text
# import dagshub
# import pickle
# import pandas as pd
# import json
# import os
# from mlflow.tracking import MlflowClient
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Retrieve the token
# dagshub_token = os.getenv('DAGSHUB_TOKEN')

# if not dagshub_token:
#     raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

# os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
# os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

# dagshub_url = "https://dagshub.com"
# repo_owner = "noman.rafique"
# repo_name = "mini-mlops-Project-ci"
# # mlflow.set_tracking_uri("https://dagshub.com/noman.rafique/mini-mlops-Project-ci.mlflow")
# mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
# vectorizer = pickle.load(open('./models/vectorizer.pkl','rb'))
# features = vectorizer.transform(["my name is nauman"])  # Vectorize the text
 

# # Generate column names dynamically based on the number of columns in the features
# num_columns = features.shape[1]
# column_names = [str(i) for i in range(num_columns)]
# data = pd.DataFrame(features.toarray(),columns=column_names)
# print(data.shape)
# print(len(vectorizer.get_feature_names_out()))


# def load_latest_model(json_file_relative_path=os.path.join('..', 'reports', 'versions.json'), model_name="my_model"):
#     def get_latest_model_version(model_name):
#         client = MlflowClient()
#         latest_version = client.get_latest_versions(model_name, stages=["Staging"])
#         print(latest_version,"1")
        
#         if not latest_version:
#             latest_version = client.get_latest_versions(model_name, stages=["None"])
#             print(latest_version,"2")
#         return latest_version[0].version if latest_version else None

#     # Step 1: Read the JSON file
#     json_file_path = os.path.join(os.path.dirname(__file__), json_file_relative_path)
    
#     # Reading the JSON file
#     with open(json_file_path, "r") as f:
#         data = json.load(f)
    
#     # Get the latest run_id using the model name
#     run_id = data.get(str(get_latest_model_version(model_name)))
    
#     # Construct the logged model path
#     logged_model = f'runs:/{run_id}/Logistic Regression'

#     # Load model as a PyFuncModel
#     model = mlflow.pyfunc.load_model(logged_model)
    
#     return model

# model = load_latest_model()
# print(model)
# print(model.predict(data))
