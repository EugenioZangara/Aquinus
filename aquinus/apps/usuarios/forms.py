# forms.py
from django import forms
from django.forms import IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

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
            fields = ['username','first_name', 'last_name', 'email']
            widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre/s'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido/s'}),
        }
            
class PerfilEditForm(forms.ModelForm):
    class Meta:
            model = Perfil
            fields = ['dni', 'es_profesor', 'puede_calificar']
            widgets = {
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI (sin puntos)'}),
            'es_profesor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_calificar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
            
            


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre/s'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido/s'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['dni', 'es_profesor', 'puede_calificar']
        widgets = {
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI (sin puntos)'}),
            'es_profesor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_calificar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User  # El modelo de usuario si es necesario
        fields = ['old_password', 'new_password1', 'new_password2']  # Campos que quieres usar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar widgets
        self.fields['old_password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña actual'
        })
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nueva contraseña'
        })
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirmar nueva contraseña'
        })