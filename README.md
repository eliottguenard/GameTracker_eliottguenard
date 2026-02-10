# GameTracker - Analyse des performances de joueurs de jeux vidéo

Pipeline ETL (Extract, Transform, Load) via docker qui analyse les performances des joueurs de jeux vidéo à partir de fichiers CSV, nettoie les données, les charge dans une base MySQL et génère un rapport de synthèse.

## Prérequis techniques

- **Docker** et **Docker Compose** installés
- **Git** pour le versionnement

## Instructions de lancement

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd mini-projet-Eliott-Guénard

# 2. Construire et démarrer les services
docker-compose up --build

# 3. Consulter le rapport généré
cat output/rapport.txt

# 4. Arrêter les services
docker-compose down

# Pour tout réinitialiser (supprimer la base de données)
docker-compose down -v
```

## Structure du projet

```
mini-projet-Eliott-Guénard/
├── Dockerfile                  # Image Python 3.11-slim avec client MySQL
├── docker-compose.yml          # Services db (MySQL 8.0) et app (Python)
├── requirements.txt            # Dépendances : mysql-connector-python, pandas
├── .gitignore                  # Fichiers ignorés par Git
├── README.md                   # Ce fichier
├── data/
│   └── raw/
│       ├── Players.csv         # Données brutes des joueurs
│       └── Scores.csv          # Données brutes des scores
├── scripts/
│   ├── init-db.sql             # Création des tables players et scores
│   ├── wait-for-db.sh          # Attente de disponibilité MySQL (30 tentatives)
│   └── run_pipeline.sh         # Script d'automatisation du pipeline complet
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration via variables d'environnement
│   ├── database.py             # Connexion MySQL avec retry et context manager
│   ├── extract.py              # Lecture des fichiers CSV
│   ├── transform.py            # Nettoyage et transformation des données
│   ├── load.py                 # Chargement en base (INSERT ON DUPLICATE KEY)
│   ├── main.py                 # Orchestration du pipeline ETL
│   └── report.py               # Génération du rapport de synthèse
└── output/
    └── rapport.txt             # Rapport généré par le pipeline
```

## Description des problèmes de qualité traités

### Players.csv

| Problème | Exemple | Traitement |
|---|---|---|
| **Doublons sur player_id** | player_id 10 = player_id 1 (ShadowBlade) | Suppression via `drop_duplicates(subset=['player_id'])` |
| **Doublons sur username** | NightWolf (id 4 et 15) après strip | Suppression via `drop_duplicates(subset=['username'])` |
| **Espaces dans les usernames** | `  StarGazer  `, `  NightWolf  ` | Nettoyage via `str.strip()` |
| **Emails invalides (sans @)** | `nightwolf` (pas d'@) | Remplacés par `None` |
| **Emails manquants** | PhoenixRider, CosmicDust | Conservés comme `None` |
| **Dates au mauvais format** | `15/03/2023`, `30-02-2024` | Converties via `pd.to_datetime(errors='coerce')` → `None` |
| **Dates invalides** | `date_inconnue` | Converties en `None` |

### Scores.csv

| Problème | Exemple | Traitement |
|---|---|---|
| **Doublons sur score_id** | SCR024 = doublon de SCR001 | Suppression via `drop_duplicates(subset=['score_id'])` |
| **Score négatif** | SCR011 : score = -500 | Suppression (filtre `score > 0`) |
| **Scores manquants** | SCR015, SCR035 : score vide | Suppression après conversion numérique |
| **Dates invalides** | SCR021 : `date_invalide` | Converties via `pd.to_datetime(errors='coerce')` → `NaT` |
| **player_id orphelin** | SCR040 : player_id = 99 (inexistant) | Suppression via filtre `valid_player_ids` |

## Auteur

Eliott Guénard - BUT Science des Données - Université de Poitiers
