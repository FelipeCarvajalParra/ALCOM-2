# Generated by Django 5.0.7 on 2024-10-11 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('CREATE', 'Crear'), ('EDIT', 'Editar'), ('DELETE', 'Eliminar'), ('LOGIN', 'Iniciar sesión'), ('LOCKOUT', 'Bloquear')], max_length=25)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
                ('category', models.CharField(blank=True, choices=[('CATEGORY', 'Categoría'), ('TEAMS', 'Equipo'), ('STOCKS', 'Existencia'), ('INTERVENTIONS', 'Intervención'), ('USER_PROFILE', 'Usuario/Perfil'), ('PART', 'Pieza')], max_length=20, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
