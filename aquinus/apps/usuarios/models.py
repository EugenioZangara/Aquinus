from django.db import models
from django.conf import settings
# Create your models here.

class Perfil(models.Model):
    usuario=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni=models.PositiveIntegerField(unique=True)
    es_profesor=models.BooleanField(default=False)
    puede_calificar=models.BooleanField(default=False)
    activo=models.BooleanField(default=False)

    
    
    def __str__(self):
        return f'Perfil de {self.user.username}'