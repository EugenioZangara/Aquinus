from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render

class MultipleRolesRequiredMixin(AccessMixin):
    """
    Verifica que el usuario tenga al menos uno de los roles requeridos.
    """
    required_roles = []  # Lista de roles permitidos

    def has_required_roles(self):
        perfil = self.request.user.perfil
        return perfil.roles.filter(nombre__in=self.required_roles).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.has_required_roles():
            return render(request, 'errores/403-forbidden/403.html', status=403)
        return super().dispatch(request, *args, **kwargs)
