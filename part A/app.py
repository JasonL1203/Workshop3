import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from flask import Flask, request, jsonify
import os

# Chargement et prétraitement des données
def preprocess_data():
    filepath = os.path.join(os.path.dirname(__file__), 'Housing.csv')
    df = pd.read_csv(filepath)
    df.replace({'yes': 1, 'no': 0}, inplace=True)
    df['furnishingstatus'] = df['furnishingstatus'].map({'furnished': 1, 'semi-furnished': 0, 'unfurnished': 0})
    df.fillna(df.mean(), inplace=True)
    return df

# Entraînement du modèle de régression linéaire
def train_linear_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_test, y_test

# Entraînement du modèle d'arbre de décision
def train_decision_tree_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    return model, X_test, y_test

# Évaluation du modèle
def evaluate_model(model, X_test, y_test):
    prediction = model.predict(X_test)
    r2 = r2_score(y_test, prediction)
    return r2

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement et prétraitement des données au démarrage de l'application
df = preprocess_data()
X = df.drop('price', axis=1)
y = df['price']

# Entraînement des deux modèles et évaluation de leurs performances
linear_model, linear_X_test, linear_y_test = train_linear_model(X, y)
linear_model_performance = evaluate_model(linear_model, linear_X_test, linear_y_test)
print(f"Linear Model R2 score: {linear_model_performance}")

decision_tree_model, tree_X_test, tree_y_test = train_decision_tree_model(X, y)
decision_tree_model_performance = evaluate_model(decision_tree_model, tree_X_test, tree_y_test)
print(f"Decision Tree Model R2 score: {decision_tree_model_performance}")

# Route pour la prédiction avec le modèle de régression linéaire
@app.route('/predict_linear', methods=['GET'])
def predict_linear():
    try:
        # Obtenir les données de la requête
        data = request.args.to_dict()
        input_data = pd.DataFrame([data])
        
        # Nettoyer les données
        cleaned_data = clean_data(input_data)
        
        # Effectuer la prédiction
        prediction = linear_model.predict(cleaned_data)
        
        # Format de réponse standardisé
        response = {
            'model': 'linear_regression',
            'prediction': prediction.tolist()
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

# Route pour la prédiction avec le modèle d'arbre de décision
@app.route('/predict_decision_tree', methods=['GET'])
def predict_decision_tree():
    try:
        # Obtenir les données de la requête
        data = request.args.to_dict()
        input_data = pd.DataFrame([data])
        
        # Nettoyer les données
        cleaned_data = clean_data(input_data)
        
        # Effectuer la prédiction
        prediction = decision_tree_model.predict(cleaned_data)
        
        # Format de réponse standardisé
        response = {
            'model': 'decision_tree',
            'prediction': prediction.tolist()
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)