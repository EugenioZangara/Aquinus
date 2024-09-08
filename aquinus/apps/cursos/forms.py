# forms.py
from django import forms
from .models import Materia

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields=['nombre', 'abreviatura','tipo']

        widgets={
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia'}),
            'abreviatura':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Abreviatura'}),
            'tipo':forms.Select(attrs={'class':'form-control'})
        }
        
       