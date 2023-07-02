# Importations des modules


import threading                                                                # Pour les threads
import pytz                                                                     # Pour la gestion des fuseaux horaires  
import datetime                                                                 # Pour les dates
import json                     
import asyncio                                                                  # Pour les boucles asynchrones
import uuid                                                                     # Pour générer des identifiants uniques
from ChatApp.models import Message,ChatUser                                    # Import des modèles                   
from channels.generic.websocket import StopConsumer,AsyncWebsocketConsumer      # Pour les websockets
from django.conf import settings                                                # Pour accéder aux paramètres de l'application

dev = settings.MODE == settings.MODES.get("DEV")                                # varibable booléenne pour savoir si l'on est en mode DEV ou PROD

class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.chat_id = self.scope['url_route']['kwargs']['chat_id'] # récupération de l'id du prototype du client websocket à partir de l'URL
        self.group_name = f"Chat_{self.chat_id}" # nom du groupe de consommateurs websocket pour le topic spécifié
        self.disconnecting = False # booléen indiquant si le client websocket est en train de se déconnecter

        # ajout du client websocket au groupe de consommateurs websocket

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept() # autorisation de connexion du client websocket

    async def receive(self, text_data=None, bytes_data=None):
        print(self)
        return await super().receive(text_data, bytes_data)
    
    async def disconnect(self, close_code):
        """
        Méthode publique asynchrone appelée lors de la déconnexion du client websocket.
        Elle enlève le client du groupe de consommateurs websocket contenues dans l'interface de communication MQTT.
        Elle enlève le client websocket du groupe de consommateurs websocket.
        """
        self.disconnecting = True
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"Client disconnected from topic {self.topic} with close code {close_code}")
        raise StopConsumer() # arrêt du consommateur websocket


                                      