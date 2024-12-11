from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

# Create model for Hero
class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='HeroImage/')

# Create Client Sponsor
class Client(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='clients/')

    def __str__(self):
        return self.name
    
# Create model for Events
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description_court = models.TextField()
    description_longue = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    capacity = models.IntegerField()
    program = models.TextField()
    image = models.ImageField(upload_to='Evenements/')
    

    def __str__(self):
        return self.title
    
    
# Create model UserAdmin
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} Profile"
    
# Create model Reservation    
class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.name} {self.surname} to {self.event.title}"

# Create model Comment 
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    content = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name or 'Anonymous'} on {self.event.title}"

# Create model Notification
class Notification(models.Model):
    TYPE_CHOICES = [
        ('reservation', 'Réservation'),
        ('cancellation', 'Annulation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    event = models.ForeignKey('Event', on_delete=models.CASCADE) 
    message = models.TextField() 
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.user} sur l'événement {self.event}"
    
# Create model Message
