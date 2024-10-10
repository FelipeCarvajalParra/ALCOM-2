from django.db import models
from apps.references.models import Referencias
from apps.categories.models import Campo

class Equipos(models.Model):
    cod_equipo_pk = models.IntegerField(primary_key=True)
    referencia_fk = models.ForeignKey(Referencias, models.DO_NOTHING, db_column='referencia_fk')
    serial = models.CharField(max_length=250)
    estado = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipos'

class Valor(models.Model):
    id_pk = models.IntegerField(primary_key=True)
    referencia_fk = models.ForeignKey(Referencias, models.DO_NOTHING, db_column='referencia_fk', blank=True, null=True)
    campo_fk = models.ForeignKey(Campo, models.DO_NOTHING, db_column='campo_fk', blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valor'