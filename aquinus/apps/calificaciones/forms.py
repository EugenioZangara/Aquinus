from django import forms
from apps.cursos.models import Calificaciones
from django.core.exceptions import ValidationError


class CalificacionesForm(forms.ModelForm):
    class Meta:
        model = Calificaciones
        fields = ['valor', 'fecha_examen']
        widgets = {
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10, 'step': 0.1}),
            'fecha_examen': forms.DateInput(attrs={'class': 'form-control fecha_examen_individual', 'type': 'date'}),
        }
    def __init__(self, *args, fechas_periodo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valor'].required = False
        self.fields['fecha_examen'].required = False
        # Asegúrate de que fechas_periodo sea pasado y contiene fechas válidas
        if fechas_periodo:
            fecha_inicio, fecha_fin = fechas_periodo
            
            # Modificamos los atributos min y max del widget de fecha
            self.fields['fecha_examen'].widget.attrs['min'] = fecha_inicio.strftime('%Y-%m-%d')
            self.fields['fecha_examen'].widget.attrs['max'] = fecha_fin.strftime('%Y-%m-%d')


    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None:
            # Obtenemos los valores min y max definidos en el widget
            min_valor = float(self.fields['valor'].widget.attrs.get('min', 0))
            max_valor = float(self.fields['valor'].widget.attrs.get('max', 10))

            # Validamos si el valor está fuera de los límites
            if not (min_valor <= valor <= max_valor):
                raise forms.ValidationError(f"El valor debe estar entre {min_valor} y {max_valor}.")
        return valor

    def clean_fecha_examen(self):
        fecha_examen = self.cleaned_data.get('fecha_examen')

        if fecha_examen and self.fechas_periodo:
            fecha_inicio, fecha_fin = self.fechas_periodo

            # Validamos si la fecha está fuera del rango
            if not (fecha_inicio <= fecha_examen <= fecha_fin):
                raise ValidationError(f"La fecha debe estar entre {fecha_inicio} y {fecha_fin}.")
        return fecha_examen