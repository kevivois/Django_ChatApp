from django.urls import path
from ChatApp import consumers     # Importation du fichier consumers.py


websocket_urlpatterns = [       # Définition des URLS pour les websockets
    path('chat/<str:chat_id>'),
]