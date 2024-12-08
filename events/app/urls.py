from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # URL 
    path('event/<int:id>/', event_details, name='details'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('admin-login/', administrator, name='administrator'),
]


 