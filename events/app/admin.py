from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(HeroSection)
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Reservation)

# Définir l'admin pour UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'post', 'country', 'phone', 'image')
    list_filter = ('country', 'company')
    search_fields = ('user__username', 'user__email', 'company')
    fieldsets = (
        (None, {
            'fields': ('user', 'about', 'company', 'post', 'country', 'address', 'phone', 'image')
        }),
    )
    list_per_page = 10  # Pagination
    ordering = ('user__username',)

# Enregistrement de l'admin pour UserProfile
admin.site.register(UserProfile, UserProfileAdmin)

# Inline pour afficher UserProfile dans la page utilisateur
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Personnalisation de l'admin de User pour inclure UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,) 
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',) 

# Désenregistrer et réenregistrer le modèle User avec la nouvelle configuration
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)