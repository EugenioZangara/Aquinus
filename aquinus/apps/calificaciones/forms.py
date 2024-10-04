from django import forms
from apps.cursos.models import Calificaciones


class CalificacionesForm(forms.ModelForm):
    class Meta:
        model = Calificaciones
        fields = ['valor', 'fecha_examen']
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.1}),
            'fecha_examen': forms.DateInput(attrs={'class': 'form-control fecha_examen_individual', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].required = False
        self.fields['fecha_examen'].required = False

    
