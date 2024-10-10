# Generated by Django 5.0.7 on 2024-10-10 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('cod_equipo_pk', models.IntegerField(primary_key=True, serialize=False)),
                ('serial', models.CharField(max_length=250)),
                ('estado', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'equipos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Valor',
            fields=[
                ('id_pk', models.IntegerField(primary_key=True, serialize=False)),
                ('valor', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'valor',
                'managed': False,
            },
        ),
    ]
