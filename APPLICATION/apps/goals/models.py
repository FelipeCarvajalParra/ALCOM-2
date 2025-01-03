from django.db import models
from apps.users.models import CustomUser

class Metas(models.Model):
    meta_id = models.AutoField(primary_key=True)
    meta = models.IntegerField()
    progreso = models.IntegerField(default=0)
    fecha_creacion = models.DateField(auto_now_add=True)
    rango_fechas = models.CharField(max_length=50, default='')
    completado = models.BooleanField(default=False)
    usuario_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='usuario_fk', blank=True, null=True)