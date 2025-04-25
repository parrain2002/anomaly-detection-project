
# api/schemas.py

from pydantic import BaseModel
from typing import Literal

class LogInput(BaseModel):
    ip: str
    user: str
    method: str
    endpoint: str
    status: int
    model_type: Literal["isolation_forest", "one_class_svm"]
    time_period: str  # Ajout du time_period
    ip_type: str      # Ajout du type d'IP
    status_class: str # Ajout de la classe de statut
    day_of_week: str  # Ajout du jour de la semaine
    hour: int         # Ajout de l'heure