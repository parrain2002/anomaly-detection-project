# api/main.py

from fastapi import FastAPI, Depends
from api.schemas import LogInput
from celery_app import celery_app  # Importez votre instance Celery

app = FastAPI()

@app.post("/predict_async")
async def predict_log_async(log_data: LogInput):
    """
    Endpoint pour envoyer une tâche de prédiction à Celery.
    """
    task = celery_app.send_task("worker.predict_task", (log_data.dict(), log_data.model_type))
    return {"task_id": task.id, "status": "Tâche de prédiction envoyée à Celery."}

@app.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    """
    Endpoint pour récupérer le statut d'une tâche Celery.
    """
    task_result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}
