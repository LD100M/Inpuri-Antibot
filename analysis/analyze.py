
# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle

import warnings
warnings.filterwarnings("ignore")
# Load the data
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
Y = df['bot_detected'].astype(int)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform PCA to reduce dimensionality
pca = PCA()
X_pca = pca.fit_transform(X_scaled)
cumulative_explained_variance = np.cumsum(pca.explained_variance_ratio_)
n_components = np.where(cumulative_explained_variance >= 0.95)[0][0] + 1
pca = PCA(n_components=n_components)
X_pca_reduced = pca.fit_transform(X_scaled)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_pca_reduced, Y, test_size=0.2, random_state=42)

# Initialize and train MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=200, activation='relu', solver='adam', random_state=42)
mlp.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = mlp.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)


# Save the model
with open('./model0/mlp_model.pkl', 'wb') as f:
    pickle.dump(mlp, f)

# Also save the PCA and StandardScaler models
with open('./model0/pca_model.pkl', 'wb') as f:
    pickle.dump(pca, f)

with open('./model0/scaler_model.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print(f'Model Accuracy: {accuracy * 100:.2f}%')