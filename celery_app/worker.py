# worker.py
import eventlet
eventlet.monkey_patch()

from celery import Celery
import joblib
import pickle
import pandas as pd

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

# Charger le pipeline et modèles
try:
    pipeline = joblib.load("../model/preprocessing_pipeline.pkl")
    with open("../model/isolation_forest.pkl", "rb") as f:
        isolation_model = pickle.load(f)
    with open("../model/one_class_svm.pkl", "rb") as f:
        svm_model = pickle.load(f)
    print("Worker: Modèles et pipeline chargés avec succès.")
except FileNotFoundError as e:
    print(f"Worker: Erreur lors du chargement des modèles ou du pipeline: {e}")
    pipeline = None
    isolation_model = None
    svm_model = None

@app.task
def predict_task(log_dict, model_type):
    if pipeline is None or isolation_model is None or svm_model is None:
        return "Worker: Modèles ou pipeline non chargés. Impossible de prédire."

    df = pd.DataFrame([log_dict])
    try:
        features = pipeline.transform(df)
        features = features.toarray() if hasattr(features, 'toarray') else features

        model = isolation_model if model_type == "isolation_forest" else svm_model
        pred = model.predict([features[0]])[0]
        return "anomalie" if pred == -1 else "normal"
    except Exception as e:
        return f"Worker: Erreur lors de la prédiction: {e}"