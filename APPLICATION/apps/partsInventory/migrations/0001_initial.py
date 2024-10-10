# Generated by Django 5.0.7 on 2024-10-10 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('num_parte_pk', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=250, null=True)),
                ('link_consulta', models.CharField(blank=True, max_length=1000, null=True)),
                ('manual', models.CharField(blank=True, max_length=400, null=True)),
                ('total_unidades', models.IntegerField()),
                ('imagen_1', models.CharField(blank=True, max_length=400, null=True)),
                ('imagen_2', models.CharField(blank=True, max_length=400, null=True)),
                ('imagen_3', models.CharField(blank=True, max_length=400, null=True)),
                ('imagen_4', models.CharField(blank=True, max_length=400, null=True)),
                ('imagen_5', models.CharField(blank=True, max_length=400, null=True)),
            ],
            options={
                'db_table': 'inventario',
                'managed': False,
            },
        ),
    ]
