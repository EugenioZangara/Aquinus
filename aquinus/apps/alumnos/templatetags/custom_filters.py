from django import template

from apps.utils.conversorPalacios import convertirEspecialidad, convertirGrado

register = template.Library()

@register.filter(name='convertirEspecialidad')
def convertir_especialidad_filter(value):
    """
    Filtro que reutiliza la función de conversión para plantillas.
    """
    return convertirEspecialidad(value)


@register.filter(name='convertirGrado')
def convertir_grado(value):
    """
    Filtro que reutiliza la función de conversión para plantillas.
    """
    return convertirGrado(value)



