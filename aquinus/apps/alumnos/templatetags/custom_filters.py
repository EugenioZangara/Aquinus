from django import template

from apps.utils.conversorPalacios import convertirEspecialidad, convertirGrado, convertirOrientaciones

register = template.Library()

@register.filter(name='convertirEspecialidad')
def convertir_especialidad_filter(value):
    """
    Filtro que reutiliza la función de conversión para plantillas.
    """
    try:
        value=int(value)
    except:
        pass
        
    return convertirEspecialidad(value)

@register.filter(name='convertirOrientaciones')
def convertir_especialidad_filter(value):
    """
    Filtro que reutiliza la función de conversión para plantillas.
    """
    try:
        value=int(value)
    except:
        pass
    
    return convertirOrientaciones(value)

@register.filter(name='convertirGrado')
def convertir_grado(value):
    """
    Filtro que reutiliza la función de conversión para plantillas.
    """
    try:
        value=int(value)
    except:
        pass
    return convertirGrado(value)



