from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import CustomLoginForm, UserForm, PerfilForm

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
    form_class=CustomLoginForm
    
class UsuarioPerfilCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'usuarios/create_user.html'
    success_url = reverse_lazy('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['perfil_form'] = PerfilForm(self.request.POST)
        else:
            context['perfil_form'] = PerfilForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        perfil_form = context['perfil_form']

        if form.is_valid() and perfil_form.is_valid():
            # Guardar el usuario
            user = form.save()
            # Asignar el usuario al perfil y guardar el perfil
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
