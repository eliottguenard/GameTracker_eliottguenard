#!/bin/bash
# Script principal pour exécuter le pipeline ETL

set -e

echo "=== GameTracker Pipeline ==="
echo "Démarrage du pipeline ETL..."

# Attente de la base de données
bash /app/scripts/wait-for-db.sh db

# Exécution du pipeline Python
python -m src.main

echo "Pipeline terminé avec succès !"
