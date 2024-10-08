from django.db import models


class Actualizaciones(models.Model):
    actualizacion_pk = models.IntegerField(primary_key=True)
    num_orden_fk = models.ForeignKey('Intervenciones', models.DO_NOTHING, db_column='num_orden_fk')
    num_parte_fk = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='num_parte_fk', blank=True, null=True)
    accion = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actualizaciones'

class Archivos(models.Model):
    referencia_pk = models.OneToOneField('Equipos', models.DO_NOTHING, db_column='referencia_pk', primary_key=True)
    imagen_1 = models.CharField(max_length=400, blank=True, null=True)
    imagen_2 = models.CharField(max_length=400, blank=True, null=True)
    imagen_3 = models.CharField(max_length=400, blank=True, null=True)
    imagen_4 = models.CharField(max_length=400, blank=True, null=True)
    imagen_5 = models.CharField(max_length=400, blank=True, null=True)
    ficha_tecnica = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'archivos'

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
    imagen = models.CharField(max_length=400, blank=True, null=True)

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

class Componentes(models.Model):
    referencia_pk = models.OneToOneField('Equipos', models.DO_NOTHING, db_column='referencia_pk', primary_key=True)
    tipo_procesador = models.CharField(max_length=400, blank=True, null=True)
    memoria_ram = models.CharField(max_length=400, blank=True, null=True)
    almacenamiento = models.CharField(max_length=400, blank=True, null=True)
    des_pantalla = models.CharField(max_length=400, blank=True, null=True)
    puertos_fisicos_externos = models.CharField(max_length=1000, blank=True, null=True)
    puertos_fisicos_internos = models.CharField(max_length=1000, blank=True, null=True)
    tarjeta_video = models.CharField(max_length=400, blank=True, null=True)
    consumible = models.CharField(max_length=400, blank=True, null=True)
    des_videobean = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'componentes'

class Equipos(models.Model):
    referencia_pk = models.CharField(primary_key=True, max_length=250)
    categoria = models.ForeignKey(Categorias, models.DO_NOTHING, db_column='categoria')
    marca = models.CharField(max_length=50)
    accesorios = models.CharField(max_length=1000, blank=True, null=True)
    observaciones = models.CharField(max_length=1000, blank=True, null=True)
    url_consulta = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipos'

class Existencias(models.Model):
    cod_equipo_pk = models.IntegerField(primary_key=True)
    referencia_fk = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='referencia_fk')
    serial = models.CharField(max_length=250)
    estado = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'existencias'

class Intervenciones(models.Model):
    num_orden_pk = models.IntegerField(primary_key=True)
    cod_equipo_fk = models.ForeignKey(Existencias, models.DO_NOTHING, db_column='cod_equipo_fk')
    fecha_hora = models.DateTimeField(blank=True, null=True)
    tecnico = models.IntegerField(blank=True, null=True)
    procesador = models.CharField(max_length=400, blank=True, null=True)
    tarea_realizada = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.CharField(max_length=150, blank=True, null=True)
    formato = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'intervenciones'

class Inventario(models.Model):
    num_parte_pk = models.CharField(primary_key=True, max_length=250)
    nombre = models.CharField(max_length=250, blank=True, null=True)
    ubicacion = models.CharField(max_length=250, blank=True, null=True)
    link_consulta = models.CharField(max_length=1000, blank=True, null=True)
    manual = models.CharField(max_length=400, blank=True, null=True)
    total_unidades = models.IntegerField()
    imagen_1 = models.CharField(max_length=400, blank=True, null=True)
    imagen_2 = models.CharField(max_length=400, blank=True, null=True)
    imagen_3 = models.CharField(max_length=400, blank=True, null=True)
    imagen_4 = models.CharField(max_length=400, blank=True, null=True)
    imagen_5 = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'

class Valor(models.Model):
    id_pk = models.IntegerField(primary_key=True)
    referencia_fk = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='referencia_fk', blank=True, null=True)
    campo_fk = models.ForeignKey(Campo, models.DO_NOTHING, db_column='campo_fk', blank=True, null=True)
    valor = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valor'
