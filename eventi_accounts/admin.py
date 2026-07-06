from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('visualizza_gruppi',)
    fieldsets = UserAdmin.fieldsets + (
        ('Campi Personalizzati', {'fields': ('eta', 'telefono')}),
    )

    def visualizza_gruppi(self, obj):
        gruppo = obj.groups.first()
        return gruppo.name if gruppo else "-"

