#!/bin/bash
# Script principal pour exécuter le pipeline ETL complet
# S'arrête à la première erreur grâce à set -e

set -e

echo "===================================================="
echo "  GAMETRACKER - Pipeline automatisé"
echo "===================================================="

# 1. Attente de la base de données
echo ""
echo ">> Etape 1 : Attente de la base de données..."
bash /app/scripts/wait-for-db.sh
echo "   Base de données prête !"

# 2. Initialisation des tables
echo ""
echo ">> Etape 2 : Initialisation des tables..."
mysql --skip-ssl -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < /app/scripts/init-db.sql
echo "   Tables initialisées !"

# 3. Exécution du pipeline ETL Python
echo ""
echo ">> Etape 3 : Exécution du pipeline ETL..."
python -m src.main
echo "   Pipeline ETL terminé !"

# 4. Génération du rapport
echo ""
echo ">> Etape 4 : Génération du rapport..."
python -c "from src.report import generate_report; generate_report()"
echo "   Rapport généré !"

echo ""
echo "===================================================="
echo "  Pipeline terminé avec succès !"
echo "===================================================="
