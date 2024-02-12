import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from flask import Flask, request, jsonify

def preprocess_data(filepath):
    df = pd.read_csv(filepath, delimiter=',')
    # Convert binary categorical variables to numeric format
    binary_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
    for column in binary_columns:
        df[column] = df[column].map({'yes': 1, 'no': 0})
    # Assuming 'furnishingstatus' is a categorical variable with more than two categories
    # Use LabelEncoder for demonstration, though one-hot encoding might be more appropriate for non-ordinal categories
    le = LabelEncoder()
    df['furnishingstatus'] = le.fit_transform(df['furnishingstatus'])
    # Handle missing values as per your original approach or consider using more sophisticated imputation methods
    df.fillna(df.mean(), inplace=True)
    return df

# Function to train the model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    return model, X_test, y_test

# Function to evaluate the model
def evaluate_model(model, X_test, y_test):
    prediction = model.predict(X_test)
    r2 = r2_score(y_test, prediction)
    return r2

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Convert query parameters to float and handle categorical variables properly
        input_data = [float(request.args.get(key)) for key in ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']]
        input_data += [int(request.args.get(key)) for key in ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']]
        # Assuming 'furnishingstatus' is passed as its encoded value
        input_data.append(int(request.args.get('furnishingstatus')))
        prediction = model.predict([input_data])[0]
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    df = preprocess_data('Partie 1\Housing.csv')
    X = df.drop('price', axis=1)
    y = df['price']
    # Train the model and evaluate its performance
    model, X_test, y_test = train_model(X, y)
    model_performance = evaluate_model(model, X_test, y_test)
    print(f"Model R2 score: {model_performance}")
    app.run(debug=True)