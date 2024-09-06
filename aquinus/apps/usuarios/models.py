from django.db import models
from django.conf import settings
from django.core.validators import ValidationError

# Create your models here.
def validar_digitos(value):
    if len(str(value)) < 7 or len(str(value))>8:
        raise ValidationError('El DNI debe tener 8 dígitos.')
    
    
class Perfil(models.Model):
    usuario=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni=models.PositiveIntegerField(unique=True,verbose_name='DNI',
        validators=[
            validar_digitos  # Máximo: 8 dígitos
        ])
    es_profesor=models.BooleanField(default=False)
    puede_calificar=models.BooleanField(default=False)
    debe_cambiar_contraseña = models.BooleanField(default=True)  # Este campo controla si debe cambiar la contraseña


    
    
    def __str__(self):
        return f'Perfil de {self.usuario.username}'