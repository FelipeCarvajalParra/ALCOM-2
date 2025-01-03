from django.db import models
from apps.users.models import CustomUser

class Metas(models.Model):
    meta_id = models.AutoField(primary_key=True)
    meta = models.IntegerField()
    fecha_creacion = models.DateField()
    descripcion = models.TextField(max_length=500)
    completado = models.BooleanField(default=False)
    usuario_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='usuario_fk', blank=True, null=True)