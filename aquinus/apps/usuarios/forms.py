# forms.py
from django import forms
from django.forms import IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm


'''
Formulario para el login al sistema
'''
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class UserEditForm(forms.ModelForm):
    class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email']
            
class PerfilEditForm(forms.ModelForm):
    class Meta:
            model = Perfil
            fields = ['dni', 'es_profesor', 'puede_calificar']
            
            
            


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name',]
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre/s'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido/s'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['dni', 'es_profesor', 'puede_calificar']
        widgets = {
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI (sin puntos)'}),
            'es_profesor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_calificar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }