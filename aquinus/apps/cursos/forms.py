# forms.py
from django import forms
from .models import Materia, PlanEstudio

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields=['nombre', 'abreviatura','tipo']

        widgets={
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia'}),
            'abreviatura':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Abreviatura'}),
            'tipo':forms.Select(attrs={'class':'form-control'})
        }
        
class MateriaEditForm(forms.ModelForm):
    class Meta:
            model = Materia
            fields = ['nombre', 'abreviatura', 'tipo']
            widgets={
            'nombre':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia'}),
            'abreviatura':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Abreviatura'}),
            'tipo':forms.Select(attrs={'class':'form-control'})
        }

class PlanEstudioForm(forms.ModelForm):
    class Meta:
        model=PlanEstudio
        fields=['especialidad', 'anio', 'materias']

        widgets={
            'especialidad':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Abreviatura de la Especialidad'}),
            'anio':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Año de puesta en vigencia del Plan'}),
                        'materias': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),  # Cambiar el widget a CheckboxSelectMultiple

        }
        # Personalización de los labels
        labels = {
            'especialidad': 'Especialidad',
            'anio': 'Año',
            'materias': 'Materias asociadas al Plan de Estudios',
        }