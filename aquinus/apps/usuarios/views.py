from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView
from django.views import View

from .forms import CustomLoginForm, UserForm, PerfilForm

# Vista personalizada de inicio de sesión.
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # Plantilla para el login.
    redirect_authenticated_user = True  # Redirige a usuarios autenticados si intentan acceder al login.
    form_class = CustomLoginForm  # Formulario personalizado para el login.

# Vista para crear un usuario y perfil.
class UsuarioPerfilCreateView(CreateView):
    model = User  # Modelo base es User de Django.
    form_class = UserForm  # Formulario para el modelo User.
    template_name = 'usuarios/crear_usuario.html'  # Plantilla para crear el usuario.
    success_url = reverse_lazy('home')  # Redirige al home después de crear el usuario.

    def get_context_data(self, **kwargs):
        """
        Añade el formulario de perfil al contexto.
        Si es un POST, usa los datos enviados, de lo contrario, inicializa el formulario vacío.
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['perfil_form'] = PerfilForm(self.request.POST)  # Formulario de perfil con datos enviados.
        else:
            context['perfil_form'] = PerfilForm()  # Formulario de perfil vacío.
        return context

    def form_valid(self, form):
        """
        Valida el formulario de usuario y perfil.
        Si ambos son válidos, guarda el usuario y el perfil asociado.
        """
        context = self.get_context_data()  # Obtiene el contexto actual.
        perfil_form = context['perfil_form']  # Obtiene el formulario de perfil.

        if form.is_valid() and perfil_form.is_valid():
            # Guardar el usuario
            user = form.save()
            # Asignar el usuario al perfil y guardar el perfil
            perfil = perfil_form.save(commit=False)  # No guardar aún.
            perfil.usuario = user  # Relacionar el perfil con el usuario creado.
            perfil.save()  # Guardar el perfil.
            # Mensaje de éxito
            messages.success(self.request, 'Usuario y perfil creados con éxito.')
            return super().form_valid(form)  # Redirige a la URL de éxito.
        else:
            # Mensaje de error en caso de datos inválidos.
            messages.error(self.request, 'Hubo un error al crear el usuario o el perfil. Verifica los datos e inténtalo de nuevo.')
            return self.form_invalid(form)  # Redirige a la misma página mostrando los errores.


class UserListView(ListView):
    model = User
    template_name = "usuarios/ver_usuarios.html"
    context_object_name = 'usuarios'

    def get_queryset(self):
        # Hacemos un select_related para traer el perfil asociado al usuario
        # Filtramos solo los usuarios que están activos (is_active=True)
        return User.objects.filter(is_active=True).select_related('perfil')
    
class DeleteUser(View):
    success_url = reverse_lazy('usuarios:ver_usuarios')  # Redirigir al listado de usuarios

    def post(self, request, pk, *args, **kwargs):
        # Obtiene el usuario por el pk (clave primaria) o devuelve 404 si no existe
        usuario = get_object_or_404(User, pk=pk)
        
        # Cambiar el estado is_active a False para hacer la eliminación lógica
        usuario.is_active = False
        usuario.save()
        messages.success(self.request, 'Usuario eliminado con éxito.')
        # Redirigir a la URL definida en success_url
        return redirect(self.success_url)
