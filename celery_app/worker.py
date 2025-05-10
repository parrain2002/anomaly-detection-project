from celery_app.celery_instance import celery
import joblib
import pickle
import pandas as pd
import os

# Déterminer le chemin absolu du dossier racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # <-- remonte d'un niveau depuis celery_app/
model_dir = os.path.join(BASE_DIR, "..", "model")      # <-- va vers ../model/
model_dir = os.path.abspath(model_dir)                 # <-- convertit en chemin absolu

print(f"Chemin du dossier modèle utilisé : {model_dir}")

# Charger le pipeline et modèles
try:
    pipeline = joblib.load(os.path.join(model_dir, "preprocessing_pipeline.pkl"))
    with open(os.path.join(model_dir, "isolation_forest.pkl"), "rb") as f:
        isolation_model = pickle.load(f)
    with open(os.path.join(model_dir, "one_class_svm.pkl"), "rb") as f:
        svm_model = pickle.load(f)
    print("Worker: Modèles et pipeline chargés avec succès.")
except FileNotFoundError as e:
    print(f"Worker: Erreur lors du chargement des modèles ou du pipeline: {e}")
    pipeline = None
    isolation_model = None
    svm_model = None

@celery.task
def predict_task(model_type: str, log_dict: dict):
    if pipeline is None or isolation_model is None or svm_model is None:
        return {"prediction": "Modèles ou pipeline non chargés. Impossible de prédire."}

    df = pd.DataFrame([log_dict])
    try:
        features = pipeline.transform(df)
        features = features.toarray() if hasattr(features, 'toarray') else features

        model = isolation_model if model_type == "isolation_forest" else svm_model
        pred = model.predict([features[0]])[0]
        result = "anomalie" if pred == -1 else "normal"
        return {"prediction": result}
    except Exception as e:
        return {"error": f"Worker: Erreur lors de la prédiction: {e}"}

