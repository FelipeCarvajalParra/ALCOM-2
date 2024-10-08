from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from apps.users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Define los campos que quieres mostrar en la vista de edición
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'position', 'status', 'login_attempts', 'profile_picture')}),
        ('Grupos', {'fields': ('groups',)}),  # Añadir grupos directamente en el formulario
    )
    
    # Define los campos que quieres mostrar al agregar un nuevo usuario
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'position', 'status', 'profile_picture', 'groups')}),
    )

    # Campos que se mostrarán en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'position', 'status', 'login_attempts',)
    
    # Opcional: Agrega filtros en la vista de lista
    list_filter = ('status', 'position', 'groups',)

# Registra el CustomUserAdmin en el admin
admin.site.register(CustomUser, CustomUserAdmin)
