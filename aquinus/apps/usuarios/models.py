from django.db import models
from django.conf import settings
from django.core.validators import ValidationError

# Create your models here.
def validar_digitos(value):
    if len(str(value)) < 7 or len(str(value))>8:
        raise ValidationError('El DNI debe tener 8 dígitos.')
    
    
# Define las opciones de áreas y roles como modelos separados
class Area(models.Model):
    nombre = models.CharField(max_length=100, choices=[('CUERPO', 'CUERPO'), ('DOCENTE', 'DOCENTE'),
                                                       ('CAL_Y_EST', 'CALIFICACIONES Y ESTADÍSTICA'), 
                                                       ('CURSOS', 'CURSOS')])
    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=100, choices=[('PROFESOR', 'PROFESOR'), 
                                                       ('ADMINISTRADOR', 'ADMINISTRADOR'), 
                                                       ('CONSUMIDOR', 'CONSUMIDOR'), 
                                                       ('STAFF', 'STAFF')])
    def __str__(self):
        return self.nombre

# Modifica el modelo Perfil
class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.PositiveIntegerField(unique=True, verbose_name='DNI',
        validators=[
            validar_digitos  # Máximo: 8 dígitos
        ])
    es_profesor = models.BooleanField(default=False)
    puede_calificar = models.BooleanField(default=False)
    debe_cambiar_contraseña = models.BooleanField(default=True)
    
    # Usa ManyToManyField para manejar múltiples áreas y roles
    areas = models.ManyToManyField(Area)
    roles = models.ManyToManyField(Rol)
    
    tratamiento = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        tratamiento = f"{self.tratamiento} " if self.tratamiento else ""
        return f'{tratamiento} {self.usuario.first_name} {self.usuario.last_name} (DNI.:{self.dni})'