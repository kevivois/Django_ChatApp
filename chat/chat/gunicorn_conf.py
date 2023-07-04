import os
import ssl
import sys
from dotenv import load_dotenv
from django.conf import settings
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    # Ajout du répertoire parent au path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')  # Définition du module de configuration de Django
django.setup()  # Initialisation de Django

load_dotenv()       # Chargement des variables d'environnement

bind = "localhost:8080"
worker_class = "uvicorn.workers.UvicornWorker"
workers = 1                                                  # Nombre de workers pour le serveur
