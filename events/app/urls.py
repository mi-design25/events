from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),

    # Section page client
    path('event/<int:id>/', event_details, name='details'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('admin-login/', admin_login, name='admin_login'),
    path('administration/dashbord/', administration, name='administration'),
    
    # Section page administator
    path('administration/ajouts-evenements/', addEvents, name='addEvents')

]