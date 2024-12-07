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