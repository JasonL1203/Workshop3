from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# Load dataset
data = pd.read_csv('Partie 1\Housing.csv', delimiter= ',')
df = pd.DataFrame(data)

# Data preprocessing
df = df.dropna()
df['mainroad'] = df['mainroad'].map({'yes': 1, 'no': 0})
df['guestroom'] = df['guestroom'].map({'yes': 1, 'no': 0})
df['basement'] = df['basement'].map({'yes': 1, 'no': 0})
df['hotwaterheating'] = df['hotwaterheating'].map({'yes': 1, 'no': 0})
df['airconditioning'] = df['airconditioning'].map({'yes': 1, 'no': 0})
df['prefarea'] = df['prefarea'].map({'yes': 1, 'no': 0})
df['furnishingstatus'] = df['furnishingstatus'].map({'furnished': 1, 'semi-furnished': 0})

# Fill NaN values
df.fillna({'area': df['area'].mean(),
           'bedrooms': df['bedrooms'].mean(),
           'bathrooms': df['bathrooms'].mean(),
           'stories': df['stories'].mean(),
           'mainroad': 0.5,
           'guestroom': 0.5,
           'basement': 0.5,
           'hotwaterheating': 0.5,
           'airconditioning': 0.5}, inplace=True)

# Drop remaining NaN values
df = df.dropna()

# Separate features (X) and target variable (y)
X = df.drop('price', axis=1)
y = df['price']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model: Random Forest Regression
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)

# Flask route for prediction
@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Extract input parameters from request
        input_params = [float(request.args.get(feature)) for feature in X.columns]

        # Perform prediction
        prediction = rf_model.predict([input_params])[0]

        # Respond with the prediction
        response = {'prediction': prediction}
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)