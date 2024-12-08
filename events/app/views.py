from django.shortcuts import render
from .models import *

# Function pour la récuperar ou l'affichage des pages
def index(request):
    hero = HeroSection.objects.first()
    clients = Client.objects.all()
    events = Event.objects.all() 
    for event in events:
        event.program_lines = event.program.splitlines()  # Ajoutez une liste à chaque événement# Récupérer tous les événements
    return render(request, 'index.html', {
        'hero': hero,
        'clients': clients,
        'events': events
    })
    
# Function pour afficher les détails d'un événement spécifique
def event_details(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'detailsEvent.html', {'event': event})

def register(request):
    return render(request, 'register.html')
def login(request):
    return render(request, 'login.html')

# def administrator(request):
#     return render(request, 'admin/admin.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def administrator(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:  # Vérifie si l'utilisateur est un administrateur
                login(request, user)
                return redirect('/admin/')  # Redirige vers le tableau de bord admin
            else:
                messages.error(request, "Vous n'avez pas les permissions administratives.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'admin/admin.html')