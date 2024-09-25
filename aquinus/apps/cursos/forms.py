# forms.py
import datetime
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from apps.usuarios.models import Perfil
from .models import Materia, PlanEstudio, Curso, Cursante, Profesor, FechasExamenes, REGIMEN_MATERIAS_CHOICES

import logging
from django.contrib.auth import get_user_model
from django_select2 import forms as s2forms

User = get_user_model()

logger = logging.getLogger(__name__)


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
    # anio = forms.ChoiceField(
    #     choices=[
    #         ("1", 'Primer Año'),
    #         ("2", 'Segundo Año'),
    #         ("3", 'Tercer Año')
    #     ],
    #     widget=forms.Select(attrs={'class': 'form-control anio',
    #                                'hx-get': "/alumnos/alumnosPorEspecialidad",  # Ruta donde envías la solicitud
    #             'hx-trigger': "change",
    #             'hx-target': "#listadoAspirantes",  # ID del contenedor que HTMX actualizará
    #             'hx-include':"[name='plan_de_estudio']", }),
    #     label='Año del curso:'
    # )

    class Meta:
        model = Curso
        fields = ['plan_de_estudio', 'division', 'anio']
        widgets = {
            'plan_de_estudio': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': "/alumnos/alumnosPorEspecialidad",  # Ruta donde envías la solicitud
                'hx-trigger': "change",
                'hx-target': "#listadoAspirantes",  # ID del contenedor que HTMX actualizará
                'hx-include':"[name='anio']",
                 
            }),
            'division': forms.NumberInput(attrs={'class': 'form-control'}),
            'anio':forms.Select(attrs={'class': 'form-control anio',
                                   'hx-get': "/alumnos/alumnosPorEspecialidad",  # Ruta donde envías la solicitud
                                    'hx-trigger': "change",
                                    'hx-target': "#listadoAspirantes",  # ID del contenedor que HTMX actualizará
                                    'hx-include':"[name='plan_de_estudio']", })
                    }
        
        labels = {
            'plan_de_estudio': 'Especialidad del curso a abrir:',
            'division': 'Ingrese la división del Curso:',
            'anio':'Año del curso:'
        }
    def __init__(self, *args, **kwargs):
        super(CursoCreateForm, self).__init__(*args, **kwargs)
        # Filtrar solo los planes de estudio cuyo campo 'vigente' sea True
    
        self.fields['plan_de_estudio'].queryset = PlanEstudio.objects.filter(vigente=True)
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Curso.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('El curso para esa especialidad y división ya existe. Por favor, verifique especialidad y división.')
        return nombre




User = get_user_model()

class AsignarProfesoresForm(forms.Form):
    usuario = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'class': 'js-example-basic-multiple',
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.select_related('perfil').filter(perfil__es_profesor=True)
        self.fields['usuario'].label = None
        self.fields['usuario'].label_from_instance = self.label_usuario

    def label_usuario(self, obj):
        if hasattr(obj, 'perfil'):
            tratamiento = f"{obj.perfil.tratamiento} " if obj.perfil.tratamiento else ""
            return f"{tratamiento} {obj.first_name} {obj.last_name} - DNI: {obj.perfil.dni}"
        else:
            return f"{obj.first_name} {obj.last_name} - Sin DNI"
        
        
class FechasCreateForm(forms.Form):
    anio_lectivo = forms.IntegerField(
        initial=datetime.date.today().year,
        label="Año Lectivo",
        required=True
    )
    fecha_inicio_ciclo_lectivo = forms.DateField(
        widget=forms.HiddenInput(attrs={'id': 'fecha_inicio_ciclo_lectivo_oculta', 'class':'fecha_inicio_ciclo_lectivo_oculta'}),
        required=True
    )
                            

    def __init__(self, *args, **kwargs):
        # Pop de kwargs para obtener el régimen de la materia, si está presente
        regimen_materia = kwargs.pop('regimen_materia', None)  # Default None si no se pasa el argumento
        super(FechasCreateForm, self).__init__(*args, **kwargs)

        # Si se ha proporcionado el régimen de la materia, construimos los campos dinámicamente
        if regimen_materia:
            match regimen_materia:
                case "ANUAL":
                    self.fields['anual_primer_trimestre'] = forms.DateField(
                        label="Fecha cierre 1er. Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['anual_segundo_trimestre'] = forms.DateField(
                        label="Fecha cierre 2do. Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['anual_tercer_trimestre'] = forms.DateField(
                        label="Fecha cierre 3er. Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['anual_cierre'] = forms.DateField(
                        label="Fecha cierre cursada: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['anual_examen_final'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    
                case "SEMESTRAL":
                    self.fields['semestral_primer_trimestre_a'] = forms.DateField(
                        label="Fecha cierre 1er. Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['semestral_cierre_a'] = forms.DateField(
                        label="Fecha cierre cursada: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['semestral_examen_final_a'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['semestral_primer_trimestre_b'] = forms.DateField(
                        label="Fecha cierre 1er. Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['semestral_cierre_b'] = forms.DateField(
                        label="Fecha cierre cursada: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['semestral_examen_final_b'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                case "CUATRIMESTRAL":
                    self.fields['cuatrimestral_primer_bimestre_a'] = forms.DateField(
                        label="Fecha cierre 1er. Bimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['cuatrimestral_cierre_a'] = forms.DateField(
                        label="Fecha cierre cursada: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['cuatrimestral_examen_final_a'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    
                    self.fields['cuatrimestral_primer_bimestre_b'] = forms.DateField(
                        label="Fecha cierre 1er. Bimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['cuatrimestral_cierre_b'] = forms.DateField(
                        label="Fecha cierre cursada: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['cuatrimestral_examen_final_b'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                case "TRIMESTRAL":
                    self.fields['primer_trimestre_cierre'] = forms.DateField(
                        label="Fecha cierre Primer Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['primer_trimestre_examen_final'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['segundo_trimestre_cierre'] = forms.DateField(
                        label="Fecha cierre Segundo Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['segundo_trimestre_examen_final'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['tercer_trimestre_cierre'] = forms.DateField(
                        label="Fecha cierre Tercer Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['tercer_trimestre_examen_final'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['cuarto_trimestre_cierre'] = forms.DateField(
                        label="Fecha cierre Cuarto Trimestre: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    self.fields['cuarto_trimestre_examen_final'] = forms.DateField(
                        label="Fecha cierre Examen Final: ",
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
                    )
                    
class AbrirComplementariosForm(forms.Form):
    numero_complementario=forms.IntegerField()
    fechaInicio=forms.DateField()
    fechaFin=forms.DateField()
    tipoMateria=forms.ChoiceField(choices=REGIMEN_MATERIAS_CHOICES)