from django.db import models
from apps.partsInventory.models import Inventario

class Compras(models.Model):
    id_compra_pk = models.AutoField(primary_key=True)
    num_parte_fk = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='num_parte_fk')  # Cambié 'Inventario' por la clase directamente
    cantidad = models.IntegerField(null=False)
    color = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now=True)
    observaciones = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.num_parte_fk} - {self.fecha}"
    
    class Meta:
        db_table = 'compras'