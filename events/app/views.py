from django.shortcuts import render
from .models import HeroSection

def index(request):
    hero = HeroSection.objects.first()  # Récupérer le premier enregistrement
    return render(request, 'index.html', {'hero': hero})

def details(request):
    return render(request, 'detailsEvent.html')