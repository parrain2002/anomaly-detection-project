# api/main.py
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import Literal
from celery import Celery
from celery.result import AsyncResult

# Importez l'instance de votre application Celery depuis le fichier celery_app.py
from celery_app.celery_app import app as celery_app

class LogData(BaseModel):
    model_type: Literal["isolation_forest", "one_class_svm"]
    ip: str
    user: str
    method: str
    endpoint: str
    status: int
    time_period: str
    ip_type: str
    status_class: str
    day_of_week: str
    hour: int

app = FastAPI()

@app.post("/predict_async/")
async def predict_log_async(log_data: LogData = Body(...)):
    task = celery_app.send_task("worker.predict_task", (log_data.dict(), log_data.model_type))
    return {"task_id": task.id}

@app.get("/task_status/{task_id}")
async def task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if not task_result.ready():
        return {"status": "PENDING"}
    result = task_result.get()
    return {"status": "SUCCESS", "result": result}