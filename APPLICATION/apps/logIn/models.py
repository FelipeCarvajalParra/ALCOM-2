from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    login_attempts = models.IntegerField(default=0)
    position = models.CharField(max_length=50, blank=True, null=True)  
    status = models.CharField(max_length=10, choices=[
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ], default='active')                    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='default/default_user.jpg')  # Asegúrate de tener Pillow instalado para trabajar con imágenes                 
