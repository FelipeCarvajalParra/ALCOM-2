# Generated by Django 5.0.7 on 2024-11-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_categoriascampo_campo_fk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorias',
            name='imagen',
            field=models.ImageField(null=True, upload_to='categories_pictures/'),
        ),
    ]
