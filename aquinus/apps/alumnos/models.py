from django.db import models

# Create your models here.
class persona(models.Model):
    grado = models.CharField(max_length=45, null=True, default=None)
    apellidos = models.CharField(max_length=45)
    nombres = models.CharField(max_length=45)
    dni = models.IntegerField(primary_key=True)
    mr = models.CharField(max_length=8, unique=True)
    # foto = models.CharField(max_length=45, null=True, default=None)
    batallon = models.CharField(max_length=45, null=True, default=None)
    compania = models.CharField(max_length=45, null=True, default=None)
    division = models.CharField(max_length=45, null=True, default=None)

    # tipo_ingreso = models.CharField(max_length=45, null=True, default=None)

    # cuil = models.CharField(max_length=11)
    sexo = models.CharField(max_length=45, null=True, default=None)
    promocion = models.IntegerField(null=True, default=None)
    especialidad = models.CharField(max_length=45, null=True, default=None)
    orientacion = models.CharField(max_length=45, null=True, default=None)
    estado = models.CharField(max_length=45, null=True, default=None)
    # fecha_nac = models.DateField(null=True, default=None)
    # email = models.CharField(max_length=45, null=True, default=None)
    # fecha_ing = models.DateField(null=True, default=None)
    # fecha_egre = models.DateField(null=True, default=None)
    # telefono_cel = models.CharField(max_length=45, null=True, default=None)
    # rol = models.CharField(max_length=45, null=True, default=None)
    # situacion = models.CharField(max_length=90, null=True, default=None)
    # nacionalidad = models.CharField(max_length=90, null=True, default=None)
    # estado_civil = models.CharField(max_length=45, null=True, default=None)
    # edad_marzo_ingreso = models.IntegerField(null=True, default=None)
    # edad_present_psp = models.IntegerField(null=True, default=None)
    # religion = models.CharField(max_length=120, null=True, default=None)
    # telefono_casa = models.CharField(max_length=45, null=True, default=None)
    # mr_mtv = models.CharField(max_length=45, null=True, default=None)
    # destino_mtv = models.CharField(max_length=45, null=True, default=None)
    # delegacion = models.CharField(max_length=90, null=True, default=None)
    # fecha_separacion = models.DateField(null=True, default=None)
    # causa_inepto = models.CharField(max_length=150, null=True, default=None)
    # observaciones = models.CharField(max_length=1000, null=True, default=None)
    # separado = models.IntegerField(null=True, default=None)

    class Meta:
        db_table = "persona"

        """ESTO ES PARA CONSULTAR SOBRE LA VISTA QUE TENGA LA RELACIÓN"""

        managed = False
        db_table = "vista_orione"
