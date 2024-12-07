from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # URL 
    path('event/<int:id>/', event_details, name='details'),
]