from django.urls import path
from  .consumers import AsyncChatConsumer


websocket_urlpatterns = [       # Définition des URLS pour les websockets
    path('chat/<str:chat_id>',AsyncChatConsumer.as_asgi()),
]