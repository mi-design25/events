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
    
    # Calcul des statistiques
    clients_count = clients.count()  
    reservations_count = Reservation.objects.count()  
    events_count = events.count() 
    comments_count = Comment.objects.count() 


    for event in events:
        event.program_lines = event.program.splitlines()

    return render(request, 'index.html', {
        'hero': hero,
        'clients': clients,
        'events': events,
        'clients_count': clients_count,
        'reservations_count': reservations_count,
        'events_count': events_count,
        'comments_count': comments_count,
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
        image = request.FILES.get('image')

        # Créer l'événement en l'associant à l'utilisateur connecté
        event = Event(
            user=request.user,
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
        event.save() 
        
        return redirect('administration')

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
    events = Event.objects.filter(user=request.user)
    return render(request, 'admin/layouts/liste_evenements.html', {'events': events})

# Function pour afficher toutes les réservations
@login_required
def liste_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'admin/layouts/liste_reservations.html', {
        'reservations': reservations
    })

# Function pour enregistrer un nouvel administrateur
def register_admin(request):
    user_form = UserRegistrationForm()
    profile_form = UserProfileForm()

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_staff = True
            user.save()

            # Créer le profil utilisateur
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_admin = True 
            profile.save()

            messages.success(request, "Votre compte administrateur a été créé avec succès.")
            return redirect('admin_login')

    return render(request, 'admin/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Function pour déconnecter l'utilisateur
def logout_view(request):
    logout(request)
    return redirect('admin_login')

# Function pour afficher les détails d'un événement
@login_required
def event_detail(request, event_id):
    reservations = Reservation.objects.filter(user=request.user)
    event = get_object_or_404(Event, id=event_id)
    comments = event.comments.all()


    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('comment')
        profile_picture = request.FILES.get('profile_picture') 

        if name and email and content:
            new_comment = Comment(
                event=event,
                name=name,
                email=email,
                content=content
            )
            if profile_picture:
                new_comment.profile_picture = profile_picture 
            new_comment.save()

    return render(request, 'event_detail.html', {'event': event, 'comments': comments,  'reservations': reservations})


# Function pour faire une reservation pour un evenements
@login_required
def reserve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id) 

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone_number = request.POST.get('number')
        email = request.POST.get('email')
        
        if Reservation.objects.filter(event=event, user=request.user).exists():
            messages.error(request, "Vous avez déjà réservé pour cet événement.")
            return redirect('event_detail', event_id=event.id)

        reservation = Reservation(
            event=event,
            user=request.user, 
            name=name,
            surname=surname,
            phone_number=phone_number,
            email=email
        )
        reservation.save()
        
        messages.success(request, "Réservation effectuée avec succès !")
        
        return redirect('event_detail', event_id=event.id)
    
    return render(request, 'event_details.html', {'event': event})

# Function pour annuler une reservation
@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if reservation:
        event_id = reservation.event.id
        reservation.delete()
        messages.success(request, "Votre réservation a été annulée avec succès.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à annuler cette réservation.")

    return redirect('event_detail', event_id=event_id)

# Function pour afficher la page profil dans l'Administrateur
@login_required
def profil(request):
    return render(request , 'admin/layouts/profil.html')
