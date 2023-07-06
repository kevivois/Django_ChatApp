from django.urls import path    # Importation de la fonction path    
from . import views             # Importation du fichier views.py

urlpatterns = [
    path('',views.home_page,name='home'),
    path('login',views.login_page,name='login'),
    path('register',views.register_page,name='register'),
    path('logout',views.logout_page,name='logout'),
    path('discussion/<str:discussion_id>',views.discussion_page,name='discussion'),
    path('create-discussion',views.create_discussion_page,name='create_discussion')
]