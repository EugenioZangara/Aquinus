# Generated by Django 5.1.1 on 2024-09-04 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfil',
            old_name='es_staff',
            new_name='activo',
        ),
    ]
