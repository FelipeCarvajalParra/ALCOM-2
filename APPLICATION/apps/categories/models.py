from django.db import models

class Campo(models.Model):
    campo_pk = models.IntegerField(primary_key=True)
    nombre_campo = models.CharField(max_length=45, blank=True, null=True)
    categoria = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campo'

class Categorias(models.Model):
    categoria_pk = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categories_pictures/', blank=True, null=True, default='default/default.jpg')

    class Meta:
        managed = False
        db_table = 'categorias'

class CategoriasCampo(models.Model):
    id_pk = models.IntegerField(primary_key=True)
    categoria_fk = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='categoria_fk')
    campo_fk = models.ForeignKey(Campo, models.DO_NOTHING, db_column='campo_fk')

    class Meta:
        managed = False
        db_table = 'categorias_campo'

