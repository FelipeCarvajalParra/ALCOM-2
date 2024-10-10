from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from apps.users.models import CustomUser
from .models import Categorias

class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('categoria_pk', 'nombre', 'imagen')  # Campos que se mostrarán en la lista
    search_fields = ('nombre',)  # Campos que se podrán buscar
    list_filter = ('nombre',)  # Filtros disponibles en la barra lateral

admin.site.register(Categorias, CategoriasAdmin)

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'position', 'status', 'login_attempts', 'profile_picture')}),
        ('Grupos', {'fields': ('groups',)}),  # Añadir grupos directamente en el formulario
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'position', 'status', 'profile_picture', 'groups')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'position', 'status', 'login_attempts',)
    list_filter = ('status', 'position', 'groups',)

# Registra el CustomUserAdmin en el admin
admin.site.register(CustomUser, CustomUserAdmin)
