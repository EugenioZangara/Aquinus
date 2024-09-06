# middleware.py
from django.shortcuts import redirect

class VerificarCambioContrasenaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            perfil = request.user.perfil  # Asumiendo que tienes un modelo Perfil relacionado
            if perfil.debe_cambiar_contraseña and request.path != '/usuarios/cambiar_contrasena/':
                return redirect('usuarios:cambiar_contrasena')

        return self.get_response(request)
