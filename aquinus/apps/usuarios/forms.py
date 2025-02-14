# forms.py
from django import forms
from django.forms import IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth import authenticate
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm


AREAS_USUARIOS=[('CUERPO', 'CUERPO'), ('DOCENTE', 'DOCENTE'),
                                                       ('CAL_Y_EST', 'CALIFICACIONES Y ESTADÍSTICA'), 
                                                       ('CURSOS', 'CURSOS')]   
ROL_USUARIOS=[('PROFESOR', 'PROFESOR'), 
                                                       ('ADMINISTRADOR', 'ADMINISTRADOR'), 
                                                       ('CONSUMIDOR', 'SOLO LECTURA'), 
                                                       ('STAFF', 'STAFF')] 

'''
Formulario para el login al sistema
'''
class CustomLoginForm(AuthenticationForm):
    dni = forms.IntegerField(widget=forms.NumberInput(attrs={'autofocus': True, "class":"form-control", "placeholder":"DNI",
                                                             'pattern': '[0-9]{7,8}', 
          
            'maxlength': '8',
            'minlength': '7',})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", 
        "placeholder": "Contraseña"
    }))   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']  # Eliminamos el campo username
    
    def clean(self):
        dni = self.cleaned_data.get('dni')
        password = self.cleaned_data.get('password')

        if dni and password:
            self.user_cache = authenticate(self.request, dni=dni, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    'DNI o contraseña incorrectos.',
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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
            fields = ['dni', 'es_profesor', 'puede_calificar', 'tratamiento']
            widgets = {
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI (sin puntos)'}),
            'es_profesor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_calificar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                        'tratamiento':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lic., Ing, TN, CC, Prof....'}),

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
        fields = ['dni', 'es_profesor', 'puede_calificar', 'tratamiento','areas', 'roles']
        widgets = {
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de DNI (sin puntos)'}),
            'es_profesor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puede_calificar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tratamiento':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lic., Ing, TN, CC, Prof....'}),
            'areas':forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple',}),
            'roles': forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple',})
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Tomar el usuario logueado
        super(PerfilForm, self).__init__(*args, **kwargs)
        # print(user.perfil.roles.all() , "rol del usuario", user.perfil.id)
        # Filtrar opciones de rol basado en el rol del usuario logueado
        if user:
            user_roles = user.perfil.roles.all()

            # Si el usuario tiene el rol "staff", puede ver todos los roles
            if user_roles.filter(nombre='STAFF').exists():
                print("valoido aca")
                # El usuario "staff" puede ver todos los roles
                self.fields['roles'].choices = ROL_USUARIOS
            elif user_roles.filter(nombre='ADMINISTRADOR').exists():
                # El "administrador" no puede ver la opción "staff"
                self.fields['roles'].choices = [role for role in ROL_USUARIOS if role[0] != 'STAFF']
            elif user.perfil.roles in ['PROFESOR', 'CONSUMIDOR']:
                # Los usuarios "profesor" o "consumidor" no pueden crear otros usuarios
                self.fields['roles'].choices = []
        
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
        
