from datetime import datetime
from django import template

from apps.cursos.models import FechasExamenes

register = template.Library()

@register.filter(name='getPeriodoCursada')
def getPeriodoCursada(periodo,tipo):
    """
    Filtro que devuelve el período de la cursada de las materias.
    """
    if periodo:
        match tipo:
            case "ANUAL":
                return "No aplica"
            case "CUATRIMESTRAL":
                return f'{periodo}° Cuatrim.'
            case "SEMESTRAL":
                return f'{periodo}° Sem.'
            case "TRIMESTRAL":
                return f'{periodo}° Trim.'
            case _:
                
                return "Desconocido"
    else: 
        if tipo=="ANUAL":
            return "No aplica"
        else:
            return "SIN ASIGNAR"

