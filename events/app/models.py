from django.db import models

# Create your models here.

# Create model for Hero
class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='HeroImage/')

