# api/model_utils.py

import pickle
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

# Charger les modèles et les pipelines au démarrage du module
try:
    with open("model/isolation_forest.pkl", "rb") as f:
        isolation_forest_model = pickle.load(f)
    with open("model/one_class_svm.pkl", "rb") as f:
        one_class_svm_model = pickle.load(f)
    with open("model/preprocessing_pipeline.pkl", "rb") as f:
        preprocessor_isoforest = joblib.load(f)
    with open("model/preprocessing_pipeline_svm.pkl", "rb") as f:
        preprocessor_svm = joblib.load(f)
    print("Modèles et pipelines chargés avec succès.")
except FileNotFoundError as e:
    print(f"Erreur lors du chargement des modèles ou des pipelines : {e}")
    isolation_forest_model = None
    one_class_svm_model = None
    preprocessor_isoforest = None
    preprocessor_svm = None

categorical_features = ["method", "endpoint", "time_period", "ip_type", "status_class", "day_of_week"]
numeric_features = ["hour"]

def preprocess_input(log_data: dict, preprocessor: ColumnTransformer):
    """Prétraite les données d'entrée pour la prédiction."""
    df = pd.DataFrame([log_data])
    # Assurez-vous que toutes les colonnes nécessaires sont présentes
    for col in categorical_features + numeric_features:
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' est manquante dans les données d'entrée.")
    return preprocessor.transform(df)

def predict_log(log_data):
    """Prédit si un log est une anomalie en utilisant le modèle spécifié."""
    model_type = log_data.model_type.lower()
    log_info = {
        "method": log_data.method,
        "endpoint": log_data.endpoint,
        "time_period": log_data.time_period,
        "ip_type": log_data.ip_type,
        "status_class": log_data.status_class,
        "day_of_week": log_data.day_of_week,
        "hour": log_data.hour
    }

    try:
        if model_type == "isolation_forest":
            if isolation_forest_model and preprocessor_isoforest:
                processed_data = preprocess_input(log_info, preprocessor_isoforest)
                prediction = isolation_forest_model.predict(processed_data)
                return "anomaly" if prediction[0] == -1 else "normal"
            else:
                return "Modèle Isolation Forest non chargé."
        elif model_type == "one_class_svm":
            if one_class_svm_model and preprocessor_svm:
                processed_data = preprocess_input(log_info, preprocessor_svm)
                prediction = one_class_svm_model.predict(processed_data)
                return "anomaly" if prediction[0] == -1 else "normal"
            else:
                return "Modèle One-Class SVM non chargé."
        else:
            return "Type de modèle non reconnu."
    except ValueError as e:
        return f"Erreur de données d'entrée: {e}"
    except Exception as e:
        return f"Erreur lors de la prédiction: {e}"
