🧠 Partie 1 - Comprendre la détection d’anomalies et son importance en Machine Learning
La détection d’anomalies est une tâche essentielle en Machine Learning, notamment dans les domaines de la cybersécurité, de la surveillance de systèmes, ou encore de la détection de fraudes. Elle permet d’identifier des comportements inhabituels au sein de grandes quantités de données, souvent dans des environnements où les étiquettes sont rares ou absentes.

🎯 Objectifs de cette première étape :
Comprendre le rôle de la détection d’anomalies dans des cas concrets

Générer un dataset réaliste de logs système

Introduire différents types d’anomalies

Visualiser et analyser les données simulées

🛠️ Étapes réalisées :
Création de la structure du projet :

data/ pour les fichiers générés

scripts/ pour les scripts Python

notebooks/ pour l’exploration et la visualisation

Génération de logs simulés :

Utilisation de Faker pour simuler des logs système

Création de logs “normaux” et “anormaux” avec des anomalies comme :

Accès non autorisés à /admin

Tentatives d’injection SQL

Floods d’une même adresse IP

Méthodes HTTP anormales (TRACE, CONNECT, etc.)

Export structuré des données :

Les logs sont sauvegardés dans un fichier CSV prêt à l’usage pour l’analyse ou l’entraînement d’un modèle

Exploration visuelle des logs dans un notebook Jupyter :

Affichage de la répartition des types de logs

Analyse temporelle des logs

Focus sur les anomalies et leurs types

📁 Fichiers principaux :
scripts/generate_logs.py : Générateur de logs simulés

data/generated_logs.csv : Fichier de logs simulés

notebooks/01_Visualisation_Logs.ipynb : Notebook d’analyse exploratoire

.gitignore : Exclusion des fichiers sensibles/temporaire
 Ce qu’on retient du code (Partie 1)
🔹 1. Génération de logs simulés (generate_logs.py)
Utilisation de la librairie faker pour créer des adresses IP, chemins d'URL, timestamps, méthodes HTTP, et statuts.

Structure d’un log simulé :
{
  "timestamp": datetime,
  "ip": str,
  "method": str,
  "url": str,
  "status": int,
  "anomaly_type": str  # "normal" ou un type d'anomalie identifié
}
Scénarios d’anomalies intégrés :

Tentatives d'accès non autorisé à /admin

Attaques de type injection SQL ('; DROP TABLE users;--)

Spams répétés d’une même adresse IP

Méthodes HTTP inhabituelles (TRACE, CONNECT, etc.)

Sauvegarde dans un CSV pour réutilisation ultérieure :
df.to_csv("data/generated_logs.csv", index=False)
🔹 2. Visualisation des logs (01_Visualisation_Logs.ipynb)
Chargement des logs avec pandas :
df = pd.read_csv("data/generated_logs.csv")
Premières statistiques :

Nombre total de logs

Répartition des types de requêtes (GET, POST...)

Fréquence des anomalies

Analyse graphique :

Histogrammes de la distribution des anomalies

Groupes par anomaly_type ou par IP pour détecter les abus

Exemple de visualisation :

df["anomaly_type"].value_counts().plot(kind="barh")
🔹 3. Gestion de projet
.gitignore mis en place pour ignorer :

Fichiers temporaires (__pycache__/, .ipynb_checkpoints/)

Environnements (.env, venv/)

Fichiers générés (*.csv)

Arborescence claire du projet pour le développement et la reproductibilité.





➡️ L’extraction de features (features = variables pertinentes)
➡️ Le feature engineering = transformer les données pour les rendre exploitables par un modèle

🔍 En quoi consiste l’Extraction & Feature Engineering Avancé ?
🔹 Objectif général
Transformer les logs bruts qu'on a générés en données structurées, pertinentes et exploitables par un algorithme de Machine Learning.



 Analyse des données de logs

🧾 Description du jeu de données

Le jeu de données étudié contient des logs web annotés selon leur type (normal ou anomalie). L’objectif est de préparer ces données pour une tâche de détection d’anomalies. Nous avons effectué plusieurs étapes essentielles de prétraitement, d’analyse et de visualisation.

⚙️ Étapes de traitement des données

1. 📥 Chargement et aperçu des données

Chargement du dataset au format CSV.

Affichage des premières lignes pour vérifier la structure.

Vérification des types de données.

2. 🧹 Nettoyage des données

Suppression des colonnes inutiles : connection_type, origin, etc.

Renommage des colonnes pour plus de clarté (response_time_ms → response_time, etc.).

Suppression des doublons.

3. 🧭 Gestion des valeurs manquantes

Aucune valeur manquante détectée.

4. 🔢 Encodage des variables catégorielles

Transformation des variables catégorielles (method, log_type, status_class, etc.) en variables numériques via encodage label ou one-hot selon les cas.

Ajout de colonnes encodées tout en conservant les originales pour vérification.

📊 Interprétation des graphiques
1. Répartition des types de logs

Ce graphique illustre la distribution des types de logs dans notre dataset. On observe une forte majorité de logs normaux, représentant environ 95% des entrées, contre seulement 5% de logs anormaux. Cette distribution déséquilibrée met en évidence un problème classique de dataset en cybersécurité, où les événements anormaux sont rares mais cruciaux à détecter. Cela implique qu’un modèle d’apprentissage supervisé devra être capable de gérer ce déséquilibre, notamment via des techniques de rééchantillonnage ou des métriques adaptées (comme la F1-score ou l’AUC).


2. Classes de statut HTTP selon le type de log

Ce second graphique compare les classes de codes HTTP (2xx, 4xx, 5xx) entre les logs normaux et les logs anormaux. Voici les observations majeures :

Les logs normaux sont principalement associés à des réponses HTTP 2xx (succès).

Les logs anormaux montrent davantage de réponses 4xx (erreurs côté client) et 5xx (erreurs serveur), bien qu’en quantité moindre.

Cela confirme que les anomalies sont corrélées à des codes d’erreur, ce qui peut servir de feature importante pour la détection automatique. En particulier, la présence d’erreurs serveur/client combinée à un log_type "anomaly" pourrait être un bon indicateur de comportements suspects ou malveillants.


# Interprétation du graphique "Période de la journée vs type de log"

**Que voyons-nous ?**

* **Axe des x (time\_period) :** Il divise la journée en quatre périodes : "afternoon" (après-midi), "night" (nuit), "evening" (soir), et "morning" (matin).
* **Axe des y (count) :** Il indique le nombre d'occurrences de chaque type de log pour chaque période de la journée.
* **Légende (log\_type) :** Il y a deux couleurs de barres : le bleu représente les logs "normal" et l'orange représente les logs "anomaly".
* **Type de graphique :** Il s'agit d'un graphique à barres groupées.

**Interprétation détaillée :**

* **Logs normaux :** L'activité normale (barres bleues) est significativement plus élevée pendant la "night" et le "morning". L'"afternoon" et l'"evening" montrent également une activité normale substantielle, mais légèrement inférieure.
* **Anomalies :** Les anomalies (barres oranges) sont relativement rares comparées aux logs normaux.
* **Distribution des anomalies par période :** Des anomalies sont présentes durant toutes les périodes, avec une légère tendance à être plus fréquentes pendant la "night" et le "morning", bien que leur nombre reste faible par rapport à l'activité normale de ces périodes.

**En résumé :**

L'activité du système (logs normaux) est la plus intense la nuit et le matin. Les anomalies se produisent à tous les moments de la journée, mais leur proportion reste faible. Une analyse plus approfondie des anomalies survenant pendant les périodes de forte activité pourrait être intéressante.




# Interprétation du graphique "Méthodes HTTP et anomalies"

**Que voyons-nous ?**

* **Axe des x (method) :** Il affiche les différentes méthodes HTTP utilisées dans les logs : POST, GET, PUT, DELETE, TRACE, et CONNECT.
* **Axe des y (count) :** Il indique le nombre d'occurrences de chaque méthode HTTP.
* **Légende (log\_type) :** Les barres bleues représentent les logs normaux, et les barres orange représentent les logs d'anomalies.
* **Type de graphique :** Il s'agit d'un graphique à barres groupées, permettant de comparer le nombre de logs normaux et d'anomalies pour chaque méthode HTTP.

**Interprétation détaillée :**

* **Méthodes principales (normales) :** Les méthodes GET, PUT, POST et DELETE sont les plus fréquemment utilisées dans les logs normaux, avec un nombre d'occurrences relativement élevé et similaire.
* **Anomalies par méthode :**
    * La méthode GET présente un nombre notable d'anomalies, bien que toujours inférieur au nombre de logs normaux pour cette méthode.
    * Les méthodes POST et PUT montrent également quelques anomalies, mais en quantité bien moindre comparée à GET.
    * La méthode DELETE ne semble présenter aucune anomalie dans cet échantillon.
    * Les méthodes TRACE et CONNECT, qui sont moins courantes dans l'activité web normale, montrent une très faible occurrence dans les logs normaux et quelques anomalies. La proportion d'anomalies par rapport aux logs normaux semble plus élevée pour ces méthodes moins fréquentes.

**En résumé :**

Les méthodes HTTP courantes (GET, PUT, POST, DELETE) constituent la majorité du trafic normal. Les anomalies sont principalement associées à la méthode GET, mais sont présentes, en moindre mesure, pour POST et PUT. Fait intéressant, les méthodes moins fréquentes comme TRACE et CONNECT, bien qu'ayant très peu d'occurrences normales, présentent quelques anomalies, ce qui pourrait indiquer une activité suspecte à examiner de plus près. La méthode DELETE, dans cet échantillon, ne montre aucune anomalie.



 Conclusion des étapes 1 & 2

Nous avons :

Nettoyé et préparé le dataset avec soin.

Réalisé des visualisations pertinentes pour mieux comprendre les relations entre les colonnes.

Encodé correctement les variables catégorielles pour une future phase de modélisation.

