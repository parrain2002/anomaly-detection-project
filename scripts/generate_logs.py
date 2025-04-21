import random                 # Pour choisir des éléments aléatoirement
import pandas as pd             # Pour manipuler et exporter les logs
from faker import Faker         # Pour générer de fausses données réalistes (IP, users, etc.)
from datetime import datetime     # Pour les horodatages

fake = Faker()                   # On initialise Faker

NUM_LOGS = 1000                  # Nombre total de logs qu’on va générer
ANOMALY_RATIO = 0.05             # 5% des logs seront des anomalies

logs = []                        # Liste où on va stocker chaque log
for _ in range(NUM_LOGS):          # On répète 1000 fois
    log_type = "normal"          # Par défaut, le log est normal
    ip = fake.ipv4()               # Adresse IP aléatoire
    user = fake.user_name()        # Nom d'utilisateur aléatoire
    method = random.choice(["GET", "POST", "PUT", "DELETE"])
    endpoint = random.choice(["/home", "/login", "/products", "/admin", "/api/data"])
    status = random.choices([200, 404, 500], weights=[80, 15, 5])[0]
    timestamp = fake.date_time_between(start_date="-30d", end_date="now")
    anomaly_type = None          # Initialisation de anomaly_type pour les logs normaux

    # 🔴 Injection d'une anomalie
    if random.random() < ANOMALY_RATIO:
        log_type = "anomaly"
        anomaly_type = random.choice(["admin_access", "sql_injection", "ip_flood", "weird_method"])

        if anomaly_type == "admin_access":
            endpoint = "/admin"
            method = "POST"
            status = 403

        elif anomaly_type == "sql_injection":
            endpoint = "/search?query=' OR 1=1 --"
            method = "GET"
            status = 500

        elif anomaly_type == "ip_flood":
            ip = "192.168.0.100"  # IP répétée pour simuler un flood
            endpoint = random.choice(["/login", "/api/data"])
            method = "GET"
            status = 429          # Too many requests

        elif anomaly_type == "weird_method":
            method = random.choice(["TRACE", "CONNECT"])
            endpoint = "/unknown"
            status = 400


    # Stocker le log
    logs.append({
        "timestamp": timestamp,
        "ip": ip,
        "user": user,
        "method": method,
        "endpoint": endpoint,
        "status": status,
        "log_type": log_type,
        "anomaly_type": anomaly_type
    })
# On crée un DataFrame à partir des logs
df = pd.DataFrame(logs)

# Exporter les logs dans un fichier CSV dans le dossier data/
df.to_csv("data/generated_logs.csv", index=False)

print("[✔] Logs générés dans '../data/generated_logs.csv'")