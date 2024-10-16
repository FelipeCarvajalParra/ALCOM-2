from django.db import models
from apps.references.models import Referencias

class Equipos(models.Model):
    cod_equipo_pk = models.IntegerField(primary_key=True)
    referencia_fk = models.ForeignKey(Referencias, models.DO_NOTHING, db_column='referencia_fk')
    serial = models.CharField(max_length=250)
    estado = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'equipos'

