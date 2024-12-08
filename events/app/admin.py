from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(HeroSection)
admin.site.register(Client)
admin.site.register(Event)

# Définir l'admin pour UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'post', 'country', 'phone', 'image')  # Champs à afficher dans la liste
    list_filter = ('country', 'company')  # Permet de filtrer par certains champs
    search_fields = ('user__username', 'user__email', 'company')  # Permet de rechercher par certains champs
    fieldsets = (
        (None, {
            'fields': ('user', 'about', 'company', 'post', 'country', 'address', 'phone', 'image')
        }),
    )

admin.site.register(UserProfile, UserProfileAdmin)

# Inline pour afficher UserProfile dans la page de l'utilisateur
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Personnaliser l'admin de User pour inclure UserProfile
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Afficher le UserProfile dans la page de l'utilisateur

    # Personnalisation de l'affichage des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')

# Enregistrer la modification de l'admin de User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)