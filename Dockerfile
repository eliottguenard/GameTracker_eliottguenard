FROM python:3.11-slim

# Installation du client MySQL
RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source et des scripts
COPY src/ ./src/
COPY scripts/ ./scripts/

# Rendre les scripts exécutables
RUN chmod +x scripts/*.sh

# Commande par défaut
CMD ["bash", "scripts/run_pipeline.sh"]
