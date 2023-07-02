import json                                                                     # Pour la conversion des données en JSON
from django.shortcuts import render, redirect                                   # Pour les redirections
from django.contrib.auth.decorators import login_required                       # Pour les permissions
from django.contrib.auth import login, logout                                   # Pour la gestion des utilisateurs
from django.contrib.auth.models import User                                     # Pour la gestion des utilisateurs
from .models import Discussion,ChatUser,Message                                           # Importation des modèles de la base de données
from django.db.models import Q
import random
@login_required(login_url='login')                          # authentification requise pour accéder à la page
def home_page(request):
    """
    Page d'accueil de l'application
    """
    print(request)
    user = request['user']
    Discussions = Discussion.objects.all()
    Discussions = [discussion for discussion in Discussions if user in discussion]
    context = {'Discussions':Discussions}
    return render(request, 'home.html',context)      

def login_page(request):
    """
    Page de connexion de l'utilisateur 
    """                         
    if request.method == 'POST':        # Si la requête est de type POST , essaie d'autentifier l'utilisateur
        email = request.POST['email']
        password = request.POST['password']                                 
        user = User.objects.get(email=email,password=password)
        if user and user.check_password(password):
            login(request,user)
            return redirect('home')                # Redirige vers la page d'accueil                          
    
    return render(request, 'login.html')            # Si la requête est de type GET, ou si l'authentification a échoué, renvoie la page de connexion


def register_page(request):
    """
    Page de création de l'utilisateur 
    """                         
    if request.method == 'POST':        # Si la requête est de type POST , essaie d'autentifier l'utilisateur
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']                                 
        user = User.objects.get(email=email)
        if not user:
            user = User.objects.get(username=username)
            if not user:
                User.objects.create(email=email,username=username,password=password)
                return redirect('home')
            else:
                print('user existing')                  
    
    return render(request, 'register.html')            # Si la requête est de type GET, ou si l'authentification a échoué, renvoie la page de connexion


@login_required(login_url='login')                      # authentification requise pour accéder à la page
def logout_page(request):
    """
    Déconnecte l'utilisateur
    """        
    logout(request)
    return redirect('login')
