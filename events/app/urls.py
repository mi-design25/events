from django.urls import path
from .views import *

urlpatterns = [
    # Page index
    path('', index, name='index'),

    # Section page client
    # Autres URLs
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('register/', register, name='register_client'),
    path('login/', login_page, name='login_client'),
    
    # Section page administator
    path('register_admin/',  register_admin, name='register'),
    path('logout/', logout_view, name='logout'),  # Ajoute cette ligne
    path('admin-login/', admin_login, name='admin_login'),
    path('administration/dashbord/', administration, name='administration'),
    path('administration/ajouts-evenements/', addEvents, name='addEvents'),
    path('administration/edit-event/<int:event_id>/', edit_event, name='edit_event'),
    path('administration/delete-event/<int:event_id>/', delete_event, name='delete_event'),
    path('administration/Liste-evenements/', liste_evenements, name='liste_evenements'),
    path('administration/Liste-reservations/', liste_reservations, name='liste_reservations')

]