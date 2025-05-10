from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from celery import Celery
import datetime
import json
from redis import Redis
from typing import Dict
from pydantic import BaseModel

class LogInput(BaseModel):
    model_type: str
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

class RawLogInput(BaseModel):
    log_line: str
    model_type: str = "isolation_forest" # Valeur par défaut

app = FastAPI()

# Configuration de la connexion Redis
redis_client = Redis(host='localhost', port=6379, db=0)

# Initialise l'application Celery directement ici (pour le test)
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@app.post("/predict_log_async/")
async def predict_log_raw_async(raw_log_input: RawLogInput):
    log_line = raw_log_input.log_line
    model_type = raw_log_input.model_type

    try:
        parts = log_line.split(',')
        if len(parts) >= 5: # Assurez-vous d'avoir au moins les champs de base
            timestamp_str = parts[0]
            ip = parts[1]
            user = parts[2]
            method = parts[3]
            endpoint_with_status = parts[4]

            endpoint_parts = endpoint_with_status.split('/')
            endpoint = "/" + "/".join(endpoint_parts[1:]) if len(endpoint_parts) > 1 else "/"
            status_str = endpoint_parts[0] if endpoint_parts[0].isdigit() else "200"
            status = int(status_str)

            # Extraction d'informations supplémentaires
            time_period = "unknown"
            hour = datetime.datetime.strptime(timestamp_str.split()[1].split(':')[0], '%H').hour
            ip_type = "unknown"
            if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.16."):
                ip_type = "private"
            else:
                ip_type = "public"

            status_class = "unknown"
            if 200 <= status < 300:
                status_class = "success"
            elif 400 <= status < 500:
                status_class = "client_error"
            elif 500 <= status < 600:
                status_class = "server_error"
            else:
                status_class = "info"

            day_of_week = datetime.datetime.strptime(timestamp_str.split()[0], '%Y-%m-%d').strftime('%A')

            log_dict = {
                "ip": ip,
                "user": user,
                "method": method,
                "endpoint": endpoint,
                "status": status,
                "time_period": time_period,
                "ip_type": ip_type,
                "status_class": status_class,
                "day_of_week": day_of_week,
                "hour": hour
            }

            task = celery_app.send_task("worker.predict_task", [model_type, log_dict])
            task_id = task.id

            # Enregistrement dans Redis (similaire à votre code)
            timestamp = datetime.datetime.now().isoformat()
            log_info = log_dict.copy()
            log_info['model_type'] = model_type
            log_info['timestamp'] = timestamp
            log_info['task_id'] = task_id
            log_info['status'] = "PENDING"

            try:
                redis_client.rpush("anomaly_logs", json.dumps(log_info))
                print(f"Informations du log brut enregistrées dans Redis (ID: {task_id})")
            except Exception as e:
                print(f"Erreur lors de l'enregistrement dans Redis: {e}")

            return JSONResponse({"task_id": task_id})
        else:
            raise HTTPException(status_code=400, detail="Format de log invalide")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du parsing du log: {e}")