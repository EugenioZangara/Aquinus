# Generated by Django 5.1.1 on 2024-09-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0018_remove_fechasexamenes_combinacion_unica_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='regimen_especial',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='materia',
            name='regimen',
            field=models.CharField(choices=[('PROMOCIONABLE', 'PROMOCIONABLE'), ('NO PROMOCIONABLE', 'NO PROMOCIONABLE')], max_length=50),
        ),
    ]
