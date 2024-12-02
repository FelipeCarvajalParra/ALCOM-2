from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    
    id = models.AutoField(primary_key=True)  # Campo ID autoincremental
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=25)
    description = models.TextField()
    link = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)  # Campo opcional para categorías
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.title} - {self.timestamp}"
    

