from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('details/', details, name='details'),  # URL pour la page de détails
]