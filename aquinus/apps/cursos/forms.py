# forms.py
import datetime
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from apps.usuarios.models import Perfil
from .models import Materia, PlanEstudio, Curso, Cursante, Profesor, FechasExamenes, REGIMEN_MATERIAS_CHOICES, Asignatura

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
    # anio_lectivo = forms.IntegerField(
    #     initial=datetime.date.today().year,
    #     label="Año Lectivo",
    #     required=True
    # )
    fecha_inicio_ciclo_lectivo = forms.DateField(
        widget=forms.TextInput(attrs={'id': 'fecha_inicio_ciclo_lectivo', 'class':'form-control', 'type':'date'}),
        required=True
    )
    aplica_para=faplica_para = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'aplica_para', 'class': 'form-select',"disabled":"true"}),
        required=False , # Aquí defines que el campo no es obligatorio
        choices=[("TODOS","Todos los años"),
                                      ("1","Primer Año"),
                                      ("2","Segundo Año"),
                                      ("3","Tercer Año"),])
    
                             

    def __init__(self, *args, **kwargs):
        # Pop de kwargs para obtener el régimen de la materia, si está presente
        regimen_materia = kwargs.pop('regimen_materia', None)  # Default None si no se pasa el argumento
        super(FechasCreateForm, self).__init__(*args, **kwargs)

        # Diccionario que contiene los nombres de los campos como claves y sus labels como valores
        campos_labels = {
            "T1": "Fecha cierre 1er. Trimestre",
            "T2": "Fecha cierre 2do. Trimestre",
            "T3": "Fecha cierre 3er. Trimestre",
            "T4": "Fecha cierre 4to. Trimestre",
            "FT_1": "Final Primer Trimestre",
            "FT_2": "Final Segundo Trimestre",
            "FT_3": "Final Tercer Trimestre",
            "FT_4": "Final Cuarto Trimestre",
            "FA": "Final Anual",
            "FS_A": "Final Primer Semestre",
            "FS_B": "Final Segundo Semestre",
            "B1_A": "Primer Bimestre - 1er. Cuatrimestre",
            "B2_A": "Cierre Primer Cuatrimestre",
            "FC_A": "Final Primer Cuatrimestre",
            "B1_B": "Primer Bimestre - 2do. Cuatrimestre",
            "B2_B": "Cierre Segundo Cuatrimestre",
            "FC_B": "Final Segundo Cuatrimestre"
        }
        
        
        '''Obtenemos los valores almacenados para definir los valores iniciales'''
        anio_lectivo=datetime.date.today().year
            
        '''
        Definimos como contexto las fechas de las materias.
        para cada régimen de materia, creamos un diccionario, cuya clave es el subperiodo y el valor es la fecha correspondiente
        '''
        fechas_anuales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="ANUAL")
        fechas_default={}
        # Inicializar las variables antes de los bucles
        inicio_ciclo_para_anuales = None
        inicio_ciclo_para_semestrales = None
        inicio_ciclo_para_cuatrimestrales = None
        inicio_ciclo_para_trimestrales = None
        for fecha in fechas_anuales_registradas:
            if fecha.subPeriodo:
                fechas_default[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            if fecha.subPeriodo=="T1":               
                inicio_ciclo_para_anuales=fecha.fechaInicioCalificacion

        fechas_semestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL")
        for fecha in fechas_semestrales_registradas:
            if fecha.subPeriodo:
                fechas_default[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            if fecha.subPeriodo=="T1":               
                inicio_ciclo_para_semestrales=fecha.fechaInicioCalificacion
        
        fechas_cuatrimestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL")
        for fecha in fechas_cuatrimestrales_registradas:
            if fecha.subPeriodo:
                fechas_default[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            if fecha.subPeriodo=="B1_A":               
                inicio_ciclo_para_cuatrimestrales=fecha.fechaInicioCalificacion
        
        fechas_trimestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL")
        for fecha in fechas_trimestrales_registradas:
            if fecha.subPeriodo:
                fechas_default[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            if fecha.subPeriodo=="T1":               
                inicio_ciclo_para_trimestrales=fecha.fechaInicioCalificacion
      
      
        # Asignar la fecha de inicio del ciclo lectivo si está disponible en el diccionario
        fecha_inicio_ciclo = next((var for var in (inicio_ciclo_para_anuales, inicio_ciclo_para_semestrales, inicio_ciclo_para_trimestrales, inicio_ciclo_para_cuatrimestrales) if var), None)


        if fecha_inicio_ciclo:
            self.fields['fecha_inicio_ciclo_lectivo'].initial = fecha_inicio_ciclo
        else:
            self.fields['fecha_inicio_ciclo_lectivo'].widget.attrs.update({'class': 'form-control bg-info'})
            
        # Iterar sobre el diccionario para asignar campos y labels personalizados
        for campo, label in campos_labels.items():
            initial_value = fechas_default.get(campo, None)
            
            # Definir las clases del campo
            field_classes = 'form-control date-input'  # Clase base para todos los campos

            # Agregar la clase 'highlight' si el campo no tiene valor inicial
            if not initial_value:
                field_classes += ' bg-info'

            self.fields[campo] = forms.DateField(
                label=label,
                required=False,
                widget=forms.TextInput(attrs={'class': field_classes, 'type': 'date'}),
                initial=initial_value
            )

                    
class PeriodoCursadaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['periodo_cursado']
        widgets={
            'periodo_cursado': forms.Select(attrs={'class':'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        # Extraer el parámetro adicional
        tipo = kwargs.pop('tipo', None)
        super(PeriodoCursadaForm, self).__init__(*args, **kwargs)
        
        # Aquí puedes utilizar el parámetro `regimen` como necesites
        if tipo == 'SEMESTRAL':
            self.fields['periodo_cursado'].choices = [('', '---------'),
                ('1', 'Primer Semestre'),
                ('2', 'Segundo Semestre')
            ]
        elif tipo == 'CUATRIMESTRAL':
            self.fields['periodo_cursado'].choices = [('', '---------'),
                ('1', 'Primer Cuatrimestre'),
                ('2', 'Segundo Cuatrimestre')
            ]
        elif tipo == 'TRIMESTRAL':
            self.fields['periodo_cursado'].choices = [('', '---------'),
                ('1', 'Primer Trimestre'),
                ('2', 'Segundo Trimestre'),
                ('3', 'Tercer Trimestre'),
                ('4', 'Cuarto Trimestre')
            ]
        else:
            # Opciones por defecto si el tipo no coincide
            self.fields['periodo_cursado'].choices = [
                ('sin_periodo', 'Sin Período Definido')
            ]
        self.fields['periodo_cursado'].widget.choices = self.fields['periodo_cursado'].choices

                    
class AbrirComplementariosForm(forms.Form):
    numero_complementario=forms.IntegerField()
    fechaInicio=forms.DateField()
    fechaFin=forms.DateField()
    tipoMateria=forms.ChoiceField(choices=REGIMEN_MATERIAS_CHOICES)