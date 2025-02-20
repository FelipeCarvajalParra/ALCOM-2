from django.db import models
from apps.references.models import Referencias

class Inventario(models.Model):
    num_parte_pk = models.CharField(primary_key=True, max_length=250)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    link_consulta = models.CharField(max_length=1000, blank=True)
    link_compra_1 = models.CharField(max_length=1000, blank=True)
    link_compra_2 = models.CharField(max_length=1000, blank=True)
    link_compra_3 = models.CharField(max_length=1000, blank=True)
    manual = models.FileField(max_length=400, blank=True, upload_to='technical_sheets/', null=True)
    total_unidades = models.IntegerField(default=0)
    imagen_1 = models.ImageField(max_length=400, blank=True, upload_to='Parts_pictures/', null=True)
    imagen_2 = models.ImageField(max_length=400, blank=True, upload_to='Parts_pictures/', null=True)
    imagen_3 = models.ImageField(max_length=400, blank=True, upload_to='Parts_pictures/', null=True)
    imagen_4 = models.ImageField(max_length=400, blank=True, upload_to='Parts_pictures/', null=True)
    imagen_5 = models.ImageField(max_length=400, blank=True, upload_to='Parts_pictures/', null=True)
    
    def __str__(self):
        return self.num_parte_pk
    
    class Meta:
        db_table = 'inventario'

class PiezasReferencias(models.Model):
    id_pk = models.AutoField(primary_key=True)
    num_parte_fk = models.ForeignKey(Inventario, on_delete=models.CASCADE, db_column='num_parte_fk')
    referencia_fk = models.ForeignKey(Referencias, on_delete=models.CASCADE, db_column='referencia_fk')

    class Meta:
        db_table = 'piezas_referencias'


