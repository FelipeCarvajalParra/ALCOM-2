from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True)  # Campo ID autoincremental
    ACTION_CHOICES = (
        ('CREATE', 'Crear'),            # Acción de crear
        ('EDIT', 'Editar'),              # Acción de editar
        ('DELETE', 'Eliminar'),          # Acción de eliminar
        ('LOGIN', 'Iniciar sesión'),     # Evento de inicio de sesión
        ('LOCKOUT', 'Bloquear'),         # Evento de bloqueo de cuenta
    )

    CATEGORY_CHOICES = (
        ('CATEGORY', 'Categoría'),            # Categoría
        ('TEAMS', 'Equipo'),                  # Equipo
        ('STOCKS', 'Existencia'),             # Existencia
        ('INTERVENTIONS', 'Intervención'),    # Intervención
        ('USER_PROFILE', 'Usuario/Perfil'),    # Usuario/Perfil
        ('PART', 'Pieza'),                     # Pieza
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=25, choices=ACTION_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)  # Campo opcional para categorías
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.title} - {self.timestamp}"
    

