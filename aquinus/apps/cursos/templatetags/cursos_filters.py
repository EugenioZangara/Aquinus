from django import template

register = template.Library()

@register.filter(name='getPeriodoCursada')
def getPeriodoCursada(periodo,tipo):
    """
    Filtro que devuelve el período de la cursada de las materias.
    """
    print(tipo,periodo)
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
