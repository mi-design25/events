from django.db import models

# Create your models here.

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