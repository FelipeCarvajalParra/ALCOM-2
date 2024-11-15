from django.db import models
from apps.equipments.models import Equipos
from apps.users.models import CustomUser

class Intervenciones(models.Model):
    num_orden_pk = models.IntegerField(primary_key=True)
    cod_equipo_fk = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='cod_equipo_fk')
    fecha_hora = models.DateTimeField(blank=True, null=True)
    usuario_fk = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)  # Cambiado a ForeignKey
    procesador = models.CharField(max_length=400, blank=True, null=True)
    tarea_realizada = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.CharField(max_length=150, blank=True, null=True)
    formato = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        db_table = 'intervenciones'

class Actualizaciones(models.Model):
    actualizacion_pk = models.AutoField(primary_key=True)
    num_orden_fk = models.ForeignKey('Intervenciones', models.DO_NOTHING, db_column='num_orden_fk', blank=True, null=True)
    num_parte_fk = models.ForeignKey('partsInventory.Inventario', models.DO_NOTHING, db_column='num_parte_fk')
    tipo_movimiento = models.CharField(max_length=50, choices=[('entrada', 'Entrada'), ('salida', 'Salida'), ('espera', 'Espera')], null=True,blank=True)
    fuente = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    color = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.CharField(max_length=250,blank=True,null=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'actualizaciones'

