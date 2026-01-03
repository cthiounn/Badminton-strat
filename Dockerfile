# Base Python slim
FROM python:3.11-slim

# Variables pour éviter warnings inutiles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY app.py requirements.txt /app/

# Installer les dépendances Python sans cache pour réduire la taille
RUN pip install --no-cache-dir -r requirements.txt

# Commande pour lancer l'application
CMD ["streamlit", "run", "app.py","--server.port", "3838"]