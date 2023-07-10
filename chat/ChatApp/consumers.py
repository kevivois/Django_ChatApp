# Importations des modules


import threading                                                                # Pour les threads
import pytz                                                                     # Pour la gestion des fuseaux horaires  
import datetime                                                                 # Pour les dates
import json                     
import asyncio                                                                  # Pour les boucles asynchrones
import uuid                                                                     # Pour générer des identifiants uniques
from ChatApp.models import Message,ChatUser,Discussion                                    # Import des modèles                   
from channels.generic.websocket import StopConsumer,AsyncWebsocketConsumer      # Pour les websockets
from django.conf import settings                                                # Pour accéder aux paramètres de l'application
from asgiref.sync import sync_to_async

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
        try:
            data = json.loads(text_data) # récupération des données envoyées par le client websocket
            user_id = data.get("user") # récupération de l'utilisateur
            user = await sync_to_async(ChatUser.objects.get)(id=user_id)
            if not user or self.chat_id != data.get("discussion") and user_id != self.scope['user'].id:
                raise Exception("User not found")
            if data.get("type") == "message":
                discussion_id = self.chat_id
                discussion = await sync_to_async(Discussion.objects.get)(id=discussion_id)
                users = await discussion.async_fetch_users()
                if user not in users:
                    raise Exception("User not in discussion")
                last_message = await sync_to_async(Message.objects.create)( 
                    user=user,
                    discussion=discussion,
                    content=data.get("content"),
                )
                await discussion.async_add_message(str(last_message.id))
            await self.channel_layer.group_send(self.group_name,{
                'type': 'chat_message',
                'message':data
            })
        except Exception as e:
            data = None
        return await super().receive(text_data, bytes_data)
    
    async def chat_message(self, event):
        """
        Méthode publique asynchrone appelée lors de la réception d'un message par le groupe de consommateurs websocket.
        Elle envoie le message au client websocket.
        """
        message = event['message']
        await self.send(text_data=json.dumps(message))
    
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
        raise StopConsumer() # arrêt du consommateur websocket


                                      