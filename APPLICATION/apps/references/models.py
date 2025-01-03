from django.db import models
from apps.categories.models import Categorias
from apps.categories.models import Campo
import os
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
 

class Referencias(models.Model):
    referencia_pk = models.CharField(primary_key=True, max_length=250, unique=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, db_column='categoria')
    marca = models.CharField(max_length=50)
    accesorios = models.CharField(max_length=1000, blank=True, null=True)
    observaciones = models.CharField(max_length=1000, blank=True, null=True)
    url_consulta = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'Referencias'

    def __str__(self):
        return self.referencia_pk

class Archivos(models.Model):
    referencia_pk = models.OneToOneField('Referencias', on_delete=models.CASCADE, db_column='referencia_pk', primary_key=True)
    imagen_1 = models.ImageField(max_length=400, blank=True, upload_to='References_pictures/', null=True)
    imagen_2 = models.ImageField(max_length=400, blank=True, upload_to='References_pictures/', null=True)
    imagen_3 = models.ImageField(max_length=400, blank=True, upload_to='References_pictures/', null=True)
    imagen_4 = models.ImageField(max_length=400, blank=True, upload_to='References_pictures/', null=True)
    imagen_5 = models.ImageField(max_length=400, blank=True, upload_to='References_pictures/', null=True)
    ficha_tecnica = models.FileField(max_length=400, blank=True, upload_to='technical_sheets/', null=True)

    class Meta:
        db_table = 'archivos'

@receiver(post_delete, sender=Archivos)
def delete_files_on_delete(sender, instance, **kwargs):
    # Elimina los archivos de imagen si existen
    for field in ['imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5', 'ficha_tecnica']:
        file = getattr(instance, field)
        if file:
            if os.path.isfile(file.path):
                os.remove(file.path)

class Valor(models.Model):
    id_pk = models.AutoField(primary_key=True)
    referencia_fk = models.ForeignKey(Referencias, on_delete=models.CASCADE, max_length=250, db_column='referencia_fk', blank=True, null=True)
    campo_fk = models.ForeignKey(Campo, on_delete=models.CASCADE, db_column='campo_fk', blank=True, null=True)
    valor = models.CharField(max_length=500, blank=True,  default='')

    class Meta:
        db_table = 'valor'
