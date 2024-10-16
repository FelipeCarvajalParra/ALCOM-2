# Generated by Django 5.0.7 on 2024-10-15 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_categoriascampo_campo_fk_and_more'),
        ('references', '0003_alter_valor_id_pk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valor',
            name='campo_fk',
            field=models.ForeignKey(blank=True, db_column='campo_fk', null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.campo'),
        ),
        migrations.AlterField(
            model_name='valor',
            name='referencia_fk',
            field=models.ForeignKey(blank=True, db_column='referencia_fk', max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, to='references.referencias'),
        ),
    ]
