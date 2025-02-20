# Generated by Django 5.1.1 on 2024-09-13 14:22

import apps.cursos.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('activo', models.BooleanField(default=False)),
                ('puede_calificar', models.BooleanField(default=False)),
                ('division', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('abreviatura', models.CharField(max_length=20)),
                ('tipo', models.CharField(choices=[('ANUAL', 'ANUAL'), ('SEMESTRAL', 'SEMESTRAL'), ('CUATRIMESTRAL', 'CUATRIMESTRAL'), ('TRIMESTRAL', 'TRIMESTRAL')], max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('regimen', models.CharField(choices=[('PROMOCIONABLE', 'PROMOCIONABLE'), ('NO PROMOCIONABLE', 'NO PROMOCIONABLE'), ('ESPECIAL', 'ESPECIAL')], max_length=50)),
                ('observaciones', models.TextField(blank=True, max_length=500, null=True)),
                ('anio', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)])),
            ],
        ),
        migrations.CreateModel(
            name='Cursante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.IntegerField()),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='alumno_curso', to='cursos.curso')),
            ],
        ),
        migrations.CreateModel(
            name='Calificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=3)),
                ('tipo', models.CharField(choices=[('BIMESTRAL', 'Bimestral'), ('TRIMESTRAL', 'Trimestral'), ('PROMEDIO CURSADA', 'Promedio Cursada'), ('EXAMEN FINAL', 'Examen Final'), ('FINAL', 'Final'), ('COMPLEMENTARIO', 'Complementario'), ('ORDINARIA', 'Ordinaria')], max_length=50)),
                ('numero_complementario', models.IntegerField(blank=True, null=True)),
                ('fecha_examen', models.DateField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('calificador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('cursante', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='nota_cursante', to='cursos.cursante')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='calificacion_materia', to='cursos.materia')),
            ],
        ),
        migrations.CreateModel(
            name='PlanEstudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(choices=[('AE', 'AE'), ('AG', 'AG'), ('AN', 'AN'), ('CO', 'CO'), ('EL', 'EL'), ('EN', 'EN'), ('FU', 'FU'), ('IM', 'IM'), ('IN', 'IN'), ('IPDSV', 'IPDSV'), ('MA', 'MA'), ('MQ', 'MQ'), ('MU', 'MU'), ('MW', 'MW'), ('OP', 'OP'), ('SH', 'SH')], max_length=10)),
                ('orientacion', models.CharField(blank=True, choices=[('ME', 'ME'), ('MS', 'MS'), ('HI', 'HI'), ('AM', 'AM'), ('AV', 'AV'), ('MC', 'MC'), ('OPCR/AC', 'OPCR/AC'), ('OPDT', 'OPDT'), ('SU', 'SU'), ('EMMH', 'EMMH'), ('AE', 'AE'), ('AEAM', 'AEAM'), ('AEAV', 'AEAV'), ('AEMC', 'AEMC'), ('AESU', 'AESU'), ('CO', 'CO'), ('EL', 'EL'), ('OC', 'OC'), ('FU', 'FU'), ('IN', 'IN'), ('CA', 'CA'), ('MO', 'MO'), ('SC', 'SC'), ('TB', 'TB'), ('MU', 'MU'), ('AA', 'AA'), ('GN', 'GN'), ('EN', 'EN'), ('BA', 'BA'), ('AC', 'AC'), ('EE', 'EE'), ('II', 'II'), ('MT', 'MT'), ('AU', 'AU'), ('EM', 'EM'), ('CC', 'CC'), ('CD', 'CD'), ('CM', 'CM'), ('PE', 'PE'), ('IM', 'IM'), ('(ITD)', '(ITD)'), ('MA', 'MA'), ('MQ', 'MQ'), ('AS', 'AS'), ('CP', 'CP'), ('CT', 'CT'), ('MN', 'MN'), ('SO', 'SO'), ('RC', 'RC'), ('EESI', 'EESI'), ('EECT', 'EECT'), ('EMAM', 'EMAM'), ('EMEL', 'EMEL'), ('RD', 'RD'), ('SR', 'SR'), ('EMPR', 'EMPR')], max_length=10, null=True)),
                ('anio', models.IntegerField(validators=[apps.cursos.models.validate_four_digits])),
                ('vigente', models.BooleanField(default=True)),
                ('materias', models.ManyToManyField(help_text='Materias asociadas al plan de estudio', related_name='materias_plan_de_estudio', to='cursos.materia')),
            ],
        ),
        migrations.AddField(
            model_name='curso',
            name='plan_de_estudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='plan_estudio_curso', to='cursos.planestudio'),
        ),
        migrations.AddIndex(
            model_name='cursante',
            index=models.Index(fields=['dni', 'curso'], name='cursos_curs_dni_4f9715_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='cursante',
            unique_together={('dni', 'curso')},
        ),
        migrations.AddConstraint(
            model_name='planestudio',
            constraint=models.UniqueConstraint(fields=('especialidad', 'anio'), name='unique_especialidad_anio'),
        ),
    ]
