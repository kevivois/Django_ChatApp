import json                                                                     # Pour la conversion des données en JSON
from django.shortcuts import render, redirect                                   # Pour les redirections
from django.contrib.auth.decorators import login_required                       # Pour les permissions
from django.contrib.auth import login, logout                                   # Pour la gestion des utilisateurs
from .models import Discussion,ChatUser,Message                                 # Importation des modèles de la base de données
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
import random
@login_required(login_url='login')                          # authentification requise pour accéder à la page
def  home_page(request):
    """
    Page d'accueil de l'application : affiche les discussions de l'utilisateur
    """

    user = request.user
    discussions = []
    for d in Discussion.objects.all():
        """
        Vérfifier si chaque d.users  est loadable en tant que json
        Si oui, on le load et on le remplace par le json
        """
        user = request.user
        if str(user.id) in d.get_users() and d.is_valid():
            d.users = d.fetch_users()
            discussions.append(d)
        
    context = {'discussions':discussions}
    return render(request, 'home.html',context)      

def login_page(request):
    """
    Page de connexion de l'utilisateur
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                print(f'user {user.email} logged -> return to home')
                return redirect('home')
            else:
                print('incorrect password')
        except User.DoesNotExist:
            print('user does not exist')

    return render(request, 'login.html')


def register_page(request):
    """
    Page de création de l'utilisateur
    """
    if request.method == 'POST':
        print('register page POST')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email,username,password)
        # Vérifier si l'utilisateur existe déjà par adresse e-mail
        if User.objects.filter(email=email).exists():
            print('user email existing')
        elif User.objects.filter(username=username).exists():
            print('user username existing')
        else:
            # Créer un nouvel utilisateur et le connecter
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return redirect('home')
        
    return render(request, 'register.html')


@login_required(login_url='login')                      # authentification requise pour accéder à la page
def logout_page(request):
    """
    Déconnecte l'utilisateur
    """        
    logout(request)
    return redirect('login')

@login_required(login_url='login')                      
def discussion_page(request,discussion_id):
    """
    Page de discussion
    """        
    user = request.user
    discussion = Discussion.objects.filter(id=discussion_id)
    if not discussion.exists():
        return redirect('home')
    discussion = discussion.get()

    if str(user.id) not in discussion.get_users():
        return redirect('home')
    
    messages = Message.objects.all()
    messages = [message for message in messages if str(message.id) in discussion.get_messages()]
    
    context = {'messages':messages,'discussion':discussion}
    return render(request, 'discussion.html',context)

@login_required(login_url='login')
def create_discussion_page(request):
    """
    Page de création de discussion
    """
    user = request.user
    users = User.objects.all().exclude(id=user.id)
    
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        
        try:
            selected_users = request.POST.getlist('users')
            if str(user.id) not in selected_users:
                selected_users.append(str(user.id))
            users_dict = {}
            users_dict['users'] = selected_users
        except:
            selected_users = []
            selected_users.append(str(user.id))
            users_dict = {}
            users_dict['users'] = selected_users
        
        Discussion.objects.create(name=name, description=description, users=users_dict)
        return redirect('discussion', discussion_id=Discussion.objects.filter(name=name, description=description).get().id)
    
    context = {'users': users}
    return render(request, 'create_discussion.html', context)

