from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(HeroSection)
admin.site.register(Client)
admin.site.register(Event)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'company', 'job', 'country', 'phone')
    search_fields = ('user__username', 'full_name', 'company', 'job', 'country')
    
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Désenregistrer le modèle User par défaut et le réenregistrer
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)