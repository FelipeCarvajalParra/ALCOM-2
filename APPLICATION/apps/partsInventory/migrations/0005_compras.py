# Generated by Django 5.0.7 on 2024-12-12 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partsInventory', '0004_inventario_link_compra_1_inventario_link_compra_2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id_compra_pk', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateField()),
                ('observaciones', models.CharField(blank=True, max_length=500, null=True)),
                ('num_parte_fk', models.ForeignKey(db_column='num_parte_fk', on_delete=django.db.models.deletion.DO_NOTHING, to='partsInventory.inventario')),
            ],
            options={
                'db_table': 'compras',
            },
        ),
    ]
