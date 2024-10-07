from django.db import models

class Categorias(models.Model):
    referencia_pk = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    campos = models.JSONField()
    imagen = models.ImageField(max_length=400, upload_to='categories/', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'categorias'

    def __str__(self):
        return str(self.referencia_pk)