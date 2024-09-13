# forms.py
from django import forms
from .models import Materia, PlanEstudio, Curso, Cursante

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
        fields=['especialidad', 'orientacion','anio', 'materias']

        widgets={
            'especialidad':forms.Select(attrs={'class': 'form-control', 'placeholder': 'Abreviatura de la Especialidad', 'name':'especialidad',
                                               'hx-get':'/cursos/get_orientaciones/', 'hx-indicator':'.htmx-indicator', 'hx-target':'#id_orientacion'}),
            'orientacion':forms.Select(attrs={'class': 'form-control', 'placeholder': 'Abreviatura de la Orientacion', 'id':'id_orientacion'}),
            'anio':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Año de puesta en vigencia del Plan'}),
                        'materias': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),  # Cambiar el widget a CheckboxSelectMultiple

        }
        # Personalización de los labels
        labels = {
            'especialidad': 'Especialidad',
            'anio': 'Año',
            'materias': 'Materias asociadas al Plan de Estudios',
        }
        
class CursoCreateForm(forms.ModelForm):
    anio = forms.ChoiceField(
        choices=[
            ("1", 'Primer Año'),
            ("2", 'Segundo Año'),
            ("3", 'Tercer Año')
        ],
        widget=forms.Select(attrs={'class': 'form-control anio',
                                   'hx-get': "/alumnos/alumnosPorEspecialidad",  # Ruta donde envías la solicitud
                'hx-trigger': "change",
                'hx-target': "#listadoAspirantes",  # ID del contenedor que HTMX actualizará
                'hx-include':"[name='plan_de_estudio']", }),
        label='Año del curso:'
    )

    class Meta:
        model = Curso
        fields = ['plan_de_estudio', 'division']
        widgets = {
            'plan_de_estudio': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': "/alumnos/alumnosPorEspecialidad",  # Ruta donde envías la solicitud
                'hx-trigger': "change",
                'hx-target': "#listadoAspirantes",  # ID del contenedor que HTMX actualizará
                'hx-include':"[name='anio']",
                 
            }),
            'division': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'plan_de_estudio': 'Especialidad del curso a abrir:',
            'division': 'Número de Divisiones del Curso:'
        }
