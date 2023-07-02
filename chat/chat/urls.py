from django.contrib import admin
from django.urls import path
from ChatApp import urls
from django.urls.conf import include    # Importation de la fonction include ppour permettre l'inclusion d'autres URLS

urlpatterns = [
    path('admin/', admin.site.urls),
     path('chat/', include('ChatApp.urls')),    # ajout de l'URL de l'application cloud
]
