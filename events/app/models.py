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
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"