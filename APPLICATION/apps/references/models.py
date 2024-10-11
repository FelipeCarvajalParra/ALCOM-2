from django.db import models
from apps.categories.models import Categorias

class Referencias(models.Model):
    referencia_pk = models.CharField(primary_key=True, max_length=250)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='categoria')
    marca = models.CharField(max_length=50)
    accesorios = models.CharField(max_length=1000, blank=True, null=True)
    observaciones = models.CharField(max_length=1000, blank=True, null=True)
    url_consulta = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'Referencias'

class Archivos(models.Model):
    referencia_pk = models.OneToOneField('Referencias', models.DO_NOTHING, db_column='referencia_pk', primary_key=True)
    imagen_1 = models.ImageField(max_length=400, blank=True, default='default/image_none.jpg', upload_to='References_pictures/', null=True)
    imagen_2 = models.ImageField(max_length=400, blank=True, default='default/image_none.jpg', upload_to='References_pictures/', null=True)
    imagen_3 = models.ImageField(max_length=400, blank=True, default='default/image_none.jpg', upload_to='References_pictures/', null=True)
    imagen_4 = models.ImageField(max_length=400, blank=True, default='default/image_none.jpg', upload_to='References_pictures/', null=True)
    imagen_5 = models.ImageField(max_length=400, blank=True, default='default/image_none.jpg', upload_to='References_pictures/', null=True)
    ficha_tecnica = models.FileField(max_length=400, blank=True, upload_to='technical_sheets/', null=True)

    class Meta:
        db_table = 'archivos'
