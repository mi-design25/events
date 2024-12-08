from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login, authenticate

from django.contrib import messages
from .models import *

# Function pour la récuperar ou l'affichage des pages
def index(request):
    hero = HeroSection.objects.first()
    clients = Client.objects.all()
    events = Event.objects.all() 
    for event in events:
        event.program_lines = event.program.splitlines()
    return render(request, 'index.html', {
        'hero': hero,
        'clients': clients,
        'events': events
    })
    
# Function pour afficher les détails d'un événement spécifique
def event_details(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'detailsEvent.html', {'event': event})

# Function pour la page de connexion
def register(request):
    return render(request, 'register.html')
def login_page(request):
    return render(request, 'login.html')

# Function pour la page d'administrateur
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('administration')
            else:
                messages.error(request, "Vous n'avez pas les permissions administratives.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'admin/admin.html')

def administration(request):
    return render(request, 'admin/layouts/index.html')

def addEvents(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description_court = request.POST.get('description_court')
        description_longue = request.POST.get('description_longue')
        location = request.POST.get('location')
        date = request.POST.get('date')
        capacity = request.POST.get('capacity')
        program = request.POST.get('program')
        image = request.FILES.get('image')  # Récupération de l'image

        # Créer l'événement
        event = Event(
            title=title,
            category=category,
            description_court=description_court,
            description_longue=description_longue,
            location=location,
            date=date,
            capacity=capacity,
            program=program,
            image=image
        )
        event.save()  # Enregistrer l'événement dans la base de données
        
        return redirect('administration')  # Redirigez vers la page d'administration ou une autre page

    return render(request, 'admin/layouts/addEvents.html')

def liste_evenements(request):
    return render(request, 'admin/layouts/liste_evenements.html')

def liste_reservations(request):
    return render(request, 'admin/layouts/liste_reservations.html')