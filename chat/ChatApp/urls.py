from django.urls import path    # Importation de la fonction path    
from . import views             # Importation du fichier views.py

urlpatterns = [
    path('',views.home_page,name='home'),
    path('login',views.login_page,name='login'),
    path('register',views.register_page,name='register'),
]