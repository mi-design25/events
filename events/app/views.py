from django.shortcuts import render
from .models import *

def index(request):
    hero = HeroSection.objects.first()  # Récupérer le premier enregistrement
    clients = Client.objects.all()  # Récupérer tous les clients
    return render(request, 'index.html', {'hero': hero, 'clients': clients})

def details(request):
    return render(request, 'detailsEvent.html')