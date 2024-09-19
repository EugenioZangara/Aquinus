from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Perfil

class DNIAuthBackend(ModelBackend):
    def authenticate(self, request, dni=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("llamo al autenticate carajo")
        try:
            # Intenta obtener el perfil con el DNI proporcionado
            
            perfil = Perfil.objects.get(dni=dni)
            user = perfil.usuario
            # Verifica la contraseña del usuario
            print(user)
            print(password)
            if user.check_password(password):
                print(user)
                return user
        except Perfil.DoesNotExist:
            # Si no se encuentra un perfil con ese DNI, retorna None
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None