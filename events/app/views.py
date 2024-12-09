from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm  
from .models import *

# Function pour afficher la page d'accueil
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

# Function pour afficher la page d'inscription
def register(request):
    return render(request, 'register.html')

# Function pour afficher la page de connexion
def login_page(request):
    return render(request, 'login.html')

# Function pour gérer la connexion à l'espace administrateur
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser or hasattr(user, 'userprofile') and user.userprofile.is_admin:
                login(request, user)
                return redirect('administration')
            else:
                messages.error(request, "Vous n'avez pas les permissions administratives.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'admin/admin.html')

# Function pour afficher l'espace administrateur personnalisé
@login_required
def administration(request):
    try:
        # Récupérer le profil de l'utilisateur connecté
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.warning(request, "Votre profil n'existe pas. Veuillez contacter l'administration.")
        return redirect('register_admin')
    
    return render(request, 'admin/layouts/index.html', {'profile': profile})

# Function pour ajouter un événement
@login_required
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

        # Créer l'événement en l'associant à l'utilisateur connecté
        event = Event(
            user=request.user,  # Associer l'utilisateur connecté
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
        
        return redirect('administration')  # Redirigez vers la page d'administration

    return render(request, 'admin/layouts/addEvents.html')

# Function pour modifier un événement
@login_required
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

# Function pour supprimer un événement
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('liste_evenements')

# Function pour afficher tous les événements
@login_required
def liste_evenements(request):
    # Filtrer les événements par utilisateur connecté
    events = Event.objects.filter(user=request.user)
    return render(request, 'admin/layouts/liste_evenements.html', {'events': events})

# Function pour afficher toutes les réservations
@login_required
def liste_reservations(request):
    return render(request, 'admin/layouts/liste_reservations.html')

# Function pour enregistrer un nouvel administrateur
def register_admin(request):
    user_form = UserRegistrationForm()
    profile_form = UserProfileForm()

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Enregistrer le mot de passe sécurisé
            user.is_staff = True
            user.save()

            # Créer le profil utilisateur
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_admin = True  # Donne des droits administratifs spécifiques à l'utilisateur
            profile.save()

            messages.success(request, "Votre compte administrateur a été créé avec succès.")
            return redirect('admin_login')

    return render(request, 'admin/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Function pour déconnecter l'utilisateur

def logout_view(request):
    # Déconnecter l'utilisateur
    logout(request)
    
    # Rediriger l'utilisateur vers la page d'accueil ou une autre page après la déconnexion
    return redirect('admin_login')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})