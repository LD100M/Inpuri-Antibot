from flask import Flask, request, jsonify, Response
import json, io, csv
from helpers.flatten_data import flatten_json
import warnings, pickle
import pandas as pd
from from_string import predict_bot_from_csv_string
import datetime

warnings.filterwarnings('ignore')

# Load the model
with open('./model0/mlp_model.pkl', 'rb') as f:
    loaded_mlp = pickle.load(f)

# Also load the PCA and StandardScaler models
with open('./model0/pca_model.pkl', 'rb') as f:
    loaded_pca = pickle.load(f)

with open('./model0/scaler_model.pkl', 'rb') as f:
    loaded_scaler = pickle.load(f)

df = pd.read_csv('data/flattened_data.csv')

# Drop irrelevant columns
drop_columns = ['_id.$oid', 'fingerprint', 'widget_id', 'bot_kind', 'bot_detection_error', 'fingerprint_confidence']
df_cleaned = df.drop(columns=drop_columns, errors='ignore')

# One-hot encode non-numeric columns
remaining_non_numeric = df_cleaned.select_dtypes(include=['object']).columns
df_cleaned = pd.get_dummies(df_cleaned, columns=remaining_non_numeric)

# Replace NaN values with 0
df_cleaned.fillna(0, inplace=True)

# Separate features and target variable
X = df_cleaned.drop('bot_detected', axis=1)

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    resp = Response("")
    resp.content_type = 'text/plain'
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    expire_date = datetime.datetime.now() + datetime.timedelta(seconds=20)
    try:
        data = json.loads(request.get_data())  # Get the JSON data from the request
        data = [flatten_json(data)]  # Flatten the data
        ogDetectionResult = data[0]["botDetected"]
        csv_data_as_string = io.StringIO()
        writer = csv.DictWriter(csv_data_as_string, fieldnames=data[0].keys())
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)
        final_string = csv_data_as_string.getvalue()
        csv_data_as_string.close()

        result = predict_bot_from_csv_string(final_string, loaded_pca, loaded_mlp, loaded_scaler, list(X.columns))
        
        print(result[1])
        if result[0] != "Bot" and not ogDetectionResult:
            resp.set_cookie('ok', '1', expires=expire_date, samesite='None', secure=True)
            resp.set_data('ok')
            return resp, 200
        else:
            resp.set_cookie('ok', '0', expires=expire_date, samesite='None', secure=True)
            resp.response = '[]'
            return resp, 400
    except Exception as e:
        print("Exception:", e)
        resp.response = str(e)
        return resp, 400

if __name__ == '__main__':
    app.run( port=4500)
