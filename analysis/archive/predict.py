
from io import StringIO
import pandas as pd

def predict_bot_from_csv_string(csv_string, pca_model, mlp_model, scaler_model, training_columns):
    """
    Predict whether a single entry is a bot or not based on a CSV-formatted string.

    Parameters:
    - csv_string (str): A string containing a single entry in CSV format.
    - pca_model (PCA object): The trained PCA model.
    - mlp_model (MLPClassifier object): The trained MLP Classifier model.
    - scaler_model (StandardScaler object): The trained Standard Scaler model.
    - training_columns (list): List of columns present in the training set after one-hot encoding.

    Returns:
    - str: "Bot" or "Not a bot" based on the prediction.
    - float: The confidence score of the prediction.
    """

    # Read the CSV string into a DataFrame
    single_entry_df = pd.read_csv(StringIO(csv_string))

    # Drop irrelevant columns
    drop_columns = ['_id.$oid', 'fingerprint', 'widget_id', 'bot_kind', 'bot_detection_error', 'fingerprint_confidence']
    single_entry = single_entry_df.drop(columns=drop_columns, errors='ignore')

    # One-hot encode categorical variables
    remaining_non_numeric = single_entry.select_dtypes(include=['object']).columns
    single_entry = pd.get_dummies(single_entry, columns=remaining_non_numeric)

    # Ensure that the one-hot encoded single entry has the same columns as the training data
    for col in training_columns:
        if col not in single_entry.columns:
            single_entry[col] = 0
    single_entry = single_entry[training_columns]

    # Handle missing values
    single_entry.fillna(0, inplace=True)

    # Standardize the features
    single_entry_scaled = scaler_model.transform(single_entry)

    # Apply PCA
    single_entry_pca = pca_model.transform(single_entry_scaled)

    # Make the prediction
    prediction = mlp_model.predict(single_entry_pca)
    prediction_proba = mlp_model.predict_proba(single_entry_pca)[:, 1]  # Probability of being a bot

    return "Bot" if prediction[0] == 1 else "Not a bot", prediction_proba[0]
