from django.urls import path
from .views import *

urlpatterns = [
    # Page index
    path('', index, name='index'),

    # Section page client
    path('event/<int:id>/', event_details, name='details'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    
    # Section page administator
    path('admin-login/', admin_login, name='admin_login'),
    path('administration/dashbord/', administration, name='administration'),
    path('administration/ajouts-evenements/', addEvents, name='addEvents'),
    path('administration/Liste-evenements/', liste_evenements, name='liste_evenements'),
    path('administration/Liste-reservations/', liste_reservations, name='liste_reservations')

]