import random                  # Pour choisir des éléments aléatoirement
import pandas as pd            # Pour manipuler et exporter les logs
from faker import Faker        # Pour générer de fausses données réalistes (IP, users, etc.)
from datetime import datetime  # Pour les horodatages
fake = Faker()                 # On initialise Faker

NUM_LOGS = 1000                # Nombre total de logs qu’on va générer
ANOMALY_RATIO = 0.05           # 5% des logs seront des anomalies

logs = []                      # Liste où on va stocker chaque log
for _ in range(NUM_LOGS):             # On répète 1000 fois
    log_type = "normal"               # Par défaut, le log est normal
    ip = fake.ipv4()                  # Adresse IP aléatoire
    user = fake.user_name()          # Nom d'utilisateur aléatoire
    method = random.choice(["GET", "POST", "PUT", "DELETE"])
    endpoint = random.choice(["/home", "/login", "/products", "/admin", "/api/data"])
    status = random.choices([200, 404, 500], weights=[80, 15, 5])[0]
    timestamp = fake.date_time_between(start_date="-30d", end_date="now")

    # 🔴 Injection d'une anomalie
    if random.random() < ANOMALY_RATIO:
        log_type = "anomaly"
        ip = fake.ipv4_private()   # Adresse IP privée suspecte
        endpoint = "/admin"        # Tentative d’accès à une zone sensible
        method = "POST"
        status = 403               # Accès refusé

    # Stocker le log
    logs.append({
        "timestamp": timestamp,
        "ip": ip,
        "user": user,
        "method": method,
        "endpoint": endpoint,
        "status": status,
        "log_type": log_type
    })
# On crée un DataFrame à partir des logs
df = pd.DataFrame(logs)

# Exporter les logs dans un fichier CSV dans le dossier data/
df.to_csv("data/generated_logs.csv", index=False)

print("[✔] Logs générés dans 'data/generated_logs.csv'")
