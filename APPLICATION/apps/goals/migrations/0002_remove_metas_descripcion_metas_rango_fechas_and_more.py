# Generated by Django 5.0.7 on 2025-01-03 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metas',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='metas',
            name='rango_fechas',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='metas',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True),
        ),
    ]
