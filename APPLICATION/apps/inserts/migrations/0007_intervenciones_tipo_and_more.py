# Generated by Django 5.0.7 on 2024-11-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inserts', '0006_rename_usuario_fk_id_intervenciones_usuario_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervenciones',
            name='tipo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='intervenciones',
            name='num_orden_pk',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
