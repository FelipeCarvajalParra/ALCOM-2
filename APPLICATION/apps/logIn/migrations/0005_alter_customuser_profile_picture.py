# Generated by Django 5.0.7 on 2024-10-02 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logIn', '0004_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default/profile.png', null=True, upload_to='profile_pictures/'),
        ),
    ]
