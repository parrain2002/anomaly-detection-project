import eventlet
eventlet.monkey_patch()

from celery import Celery
import os
import sys

# Ajoutez le chemin du dossier courant (celery_app) au sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['worker']  # Celery cherchera 'worker.py' dans les chemins Python
)