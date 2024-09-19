
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, UpdateView, FormView
from django.views import View

from .forms import CustomLoginForm, UserForm, PerfilForm, UserEditForm, PerfilEditForm, CustomPasswordChangeForm

# Vista personalizada de inicio de sesión.
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
    form_class = CustomLoginForm
    
    def get_success_url(self):
        return reverse_lazy('home')  # Asegúrate de que 'home' es el nombre correcto de tu URL

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('rememberPassword')
        if not remember_me:
            # Establece la cookie de sesión para que expire cuando el usuario cierre el navegador
            self.request.session.set_expiry(0)
        return super().form_valid(form)

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
        context['active_tab']="usuarios"
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
        if not form.is_valid():
            print("Errores en el formulario de usuario:", form.errors)
        if not perfil_form.is_valid():
            print("Errores en el formulario de perfil:", perfil_form.errors)
        if form.is_valid() and perfil_form.is_valid():
            # Guardar el usuario
            user = form.save(commit=False)
            user.set_password('armada2024')  # Puedes personalizar la contraseña genérica aquí
            user.save()  # Ahora sí, guarda el usuario con la contraseña
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="usuarios"
      
        return context
    def get_queryset(self):
        # Hacemos un select_related para traer el perfil asociado al usuario
        # Filtramos solo los usuarios que están activos (is_active=True)
        return User.objects.filter(is_active=True, is_staff=False).select_related('perfil')
    
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




class UserUpdateView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "usuarios/actualizar_usuarios.html"
    success_url = reverse_lazy('usuarios:ver_usuarios')  # Redirigir al listado de usuarios

    def get_object(self, queryset=None):
        # Obtener el pk de la URL
        pk = self.kwargs.get('pk')
        # Buscar el usuario en base al pk pasado en la URL
        return get_object_or_404(User, pk=pk)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el perfil asociado al usuario
        context['active_tab']="usuarios"
        perfil = Perfil.objects.get(usuario=self.get_object())
        
        # Si 'user_form' y 'perfil_form' no están en kwargs, crearlos
        if 'user_form' not in kwargs:
            kwargs['user_form'] = UserEditForm(instance=self.get_object())
        if 'perfil_form' not in kwargs:
            kwargs['perfil_form'] = PerfilEditForm(instance=perfil)

        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Asegúrate de definir self.object
        user_form = UserEditForm(request.POST, instance=self.object)
        perfil = Perfil.objects.get(usuario=self.object)
        perfil_form = PerfilEditForm(request.POST, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(self.request, 'Usuario modificado exitosamente')
            return redirect(self.success_url)
        else:
                     # Imprimir los errores del formulario para depuración
            print("Errores del formulario de usuario:", user_form.errors)
            print("Errores del formulario de perfil:", perfil_form.errors)
            # Si los formularios no son válidos, pasa los formularios con errores al contexto
            context = self.get_context_data(user_form=user_form, perfil_form=perfil_form)
            return self.render_to_response(context)


class CambiarContrasenaView(FormView):
    template_name = 'usuarios/cambiar_contrasena.html'  # Tu plantilla HTML para el cambio de contraseña
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')  # Redirigir a esta URL después del cambio

    def get_form_kwargs(self):
        """
        Pasa el usuario autenticado al formulario.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Si el formulario es válido, guarda la nueva contraseña y actualiza la sesión.
        """
        user = form.save()
        update_session_auth_hash(self.request, user)  # Mantiene la sesión activa
        # Marcar que el usuario ya no necesita cambiar la contraseña
        user.perfil.debe_cambiar_contraseña = False
        user.perfil.save()
        messages.success(self.request, 'Contraseña cambiada exitosamente.')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        Verifica si el usuario está autenticado y si debe cambiar la contraseña.
        """
        if not request.user.is_authenticated:
            return redirect('usuarios:login')  # Si no está autenticado, redirigir al login
        if not request.user.perfil.debe_cambiar_contraseña:
            return redirect('home')  # Si no necesita cambiar contraseña, redirigir
        return super().dispatch(request, *args, **kwargs)
    
    
class ProfesoresListView(ListView):
    model = User
    template_name = "usuarios/consulta_profesores.html"
    context_object_name='profesores'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="profesores"
      
        return context
    def get_queryset(self):
        # Hacemos un select_related para traer el perfil asociado al usuario
        # Filtramos solo los usuarios que están activos (is_active=True)
        return User.objects.filter(is_active=True, is_staff=False, perfil__es_profesor=True).select_related('perfil')
    
