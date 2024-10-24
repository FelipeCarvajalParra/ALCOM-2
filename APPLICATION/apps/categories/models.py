from django.db import models

class Campo(models.Model):
    campo_pk = models.AutoField(primary_key=True) 
    nombre_campo = models.CharField(max_length=45)

    class Meta:
        db_table = 'campo'

class Categorias(models.Model):
    categoria_pk = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='categories_pictures/', null=True)

    class Meta:
        db_table = 'categorias'

class CategoriasCampo(models.Model):
    id_pk = models.AutoField(primary_key=True)  
    categoria_fk = models.ForeignKey(Categorias, on_delete=models.CASCADE, db_column='categoria_fk', null=True) 
    campo_fk = models.ForeignKey(Campo, on_delete=models.CASCADE, db_column='campo_fk')  

    class Meta:
        db_table = 'categorias_campo'

