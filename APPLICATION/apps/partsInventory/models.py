from django.db import models

class Inventario(models.Model):
    num_parte_pk = models.CharField(primary_key=True, max_length=250)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    link_consulta = models.CharField(max_length=1000, blank=True, null=True)
    manual = models.CharField(max_length=400, blank=True, null=True)
    total_unidades = models.IntegerField()
    imagen_1 = models.CharField(max_length=400, blank=True, null=True)
    imagen_2 = models.CharField(max_length=400, blank=True, null=True)
    imagen_3 = models.CharField(max_length=400, blank=True, null=True)
    imagen_4 = models.CharField(max_length=400, blank=True, null=True)
    imagen_5 = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'

