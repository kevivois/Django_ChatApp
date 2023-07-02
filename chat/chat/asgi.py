
import os, sys,threading
import django
import ChatApp.routing
from django.core.asgi import get_asgi_application                   # Initialisation de l'application Django ASGI
from channels.routing import ProtocolTypeRouter, URLRouter          # routers pour les protocoles de communication
from channels.auth import AuthMiddlewareStack                       # Middleware d'authentification
from channels.layers import get_channel_layer                       # Channel layer
from channels.security.websocket import AllowedHostsOriginValidator # Middleware de sécurité pour les websockets

django.setup() # Initialisation de Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings')        # Définition du module de configuration de Django

django_asgi_app = get_asgi_application() # Initialisation de l'application Django ASGI

layer = get_channel_layer()     # Initialisation du channel layer


application = ProtocolTypeRouter({          # Définition du protocole de communication
    "http": django_asgi_app,                # Protocole HTTP
    "websocket": AllowedHostsOriginValidator(   # Protocole Websocket
        AuthMiddlewareStack(                    # Middleware d'authentification
            URLRouter(
                ChatApp.routing.websocket_urlpatterns     # Définition des URLS pour les websockets
            )
        )
    ),
})



