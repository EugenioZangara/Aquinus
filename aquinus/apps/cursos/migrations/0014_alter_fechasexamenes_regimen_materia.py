# Generated by Django 5.1.1 on 2024-09-23 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0013_fechasexamenes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fechasexamenes',
            name='regimen_materia',
            field=models.CharField(choices=[('BIMESTRAL', 'Bimestral'), ('TRIMESTRAL', 'Trimestral'), ('CUATRIMESTRAL', 'Cuatrimestral'), ('SEMESTRAL', 'Semestral'), ('ANUAL', 'Anual')], max_length=50),
        ),
    ]
