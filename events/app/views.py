from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

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

def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.category = request.POST.get('category')
        event.description_court = request.POST.get('description_court')
        event.description_longue = request.POST.get('description_longue')
        event.location = request.POST.get('location')
        event.date = request.POST.get('date')
        event.capacity = request.POST.get('capacity')
        event.program = request.POST.get('program')
        if request.FILES.get('image'):
            event.image = request.FILES.get('image')
        event.save()
        return redirect('liste_evenements')

    return render(request, 'admin/layouts/edit_event.html', {'event': event})
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('liste_evenements')

def liste_evenements(request):
    # Récupérer tous les événements
    events = Event.objects.all()
    return render(request, 'admin/layouts/liste_evenements.html', {'events': events})

def liste_reservations(request):
    return render(request, 'admin/layouts/liste_reservations.html')


@login_required
def create_admin(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas la permission de créer un administrateur.")
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        about = request.POST.get('about')
        full_name = request.POST.get('full_name')
        company = request.POST.get('company')
        job = request.POST.get('job')
        country = request.POST.get('country')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'create-admin.html', request.POST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True,
            )
            UserProfile.objects.create(
                user=user,
                about=about,
                company=company,
                job=job,
                country=country,
                address=address,
                phone=phone,
                image=image,
            )
            messages.success(request, "Compte administrateur créé avec succès.")
            return redirect('admin/layouts/index.html')
        except Exception as e:
            messages.error(request, f"Erreur : {e}")
    return render(request, 'admin/create-admin.html')