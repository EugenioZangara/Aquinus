from django.template.loader import render_to_string
from django.http import HttpResponse

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from apps.alumnos.models import persona
from .forms import PeriodoCursadaForm
from .models import Asignatura


combinaciones_permitidas = {
    'SH': ['ME', 'HI', 'OC', 'BA'],
    'IM': ['MS', 'AA', 'AC', 'CO', 'EE', 'II', 'MT'],
    'AE': ['AM', 'AV', 'MC', 'OPCR/AC', 'OPDT', 'SU'],
    'AN': ['EMMH', 'AE', 'AEAM', 'AEAV', 'AEMC', 'AESU', 'AU', 'EE', 'EM'],
    'CO': ['CO'],
    'EL': ['EL'],
    'FU': ['FU'],
    'IN': ['IN'],
    'MQ': ['CA', 'MO', 'SC', 'TB', 'MQ'],
    'MU': ['MU'],
    'MW': ['AA', 'AS', 'CP', 'MN', 'RC'],
    'OP': ['GN', 'SO'],
    'AG': ['CC', 'CD', 'CM', 'PE'],
    'IPDSV': ['CD', 'CM'],
    'MA': ['(ITD)', 'MA'],
    'EN':[' - ']
}
def get_orientaciones(request):
    especialidad= request.GET.get('especialidad')
    orientaciones=combinaciones_permitidas[especialidad]
    print(orientaciones)
    return render(request, 'parciales/cursos/orientaciones_choices.html', {'orientaciones':orientaciones})

'''
Funciones para funcionalidad de armada de curso, agregar y quitar alumnos del curso
'''
def seleccionar_registro(request, id):
    registro = get_object_or_404(persona.objects.using('id8'), dni=id)

    # Renderiza la nueva fila para la tabla de seleccionados
    new_row = render_to_string('parciales/cursos/selected_row.html', {'registro': registro})
    
    # Prepara la respuesta para eliminar la fila de la tabla original
    remove_row = f'<tr id="registro-{id}" hx-swap-oob="delete"></tr>'
    
    # Combina ambas respuestas
    response = f"{new_row}{remove_row}"
    
    return HttpResponse(response)

def quitar_registro(request, id):
    registro = get_object_or_404(persona.objects.using('id8'), dni=id)
    
    # Renderiza la nueva fila para la tabla de seleccionados
    new_row = render_to_string('parciales/cursos/reload_row.html', {'registro': registro})
    
    # Prepara la respuesta para eliminar la fila de la tabla original
    remove_row = f'<tr id="seleccionadoId-{id}" hx-swap-oob="delete"></tr>'
    
    # Combina ambas respuestas
    response = f"{new_row}{remove_row}"
    
    return HttpResponse(response)



'''
Funcionalidad para SOLO AGREGAR registros para modificar cursos
'''
def agregar_registro(request, id):
    registro = get_object_or_404(persona.objects.using('id8'), dni=id)

    # Renderiza la nueva fila para la tabla de seleccionados
    new_row = render_to_string('parciales/cursos/fila_agregada.html', {'registro': registro})
    
    # Prepara la respuesta para eliminar la fila de la tabla original
    remove_row = f'<tr id="registro-{id}" hx-swap-oob="delete"></tr>'
    
    # Combina ambas respuestas
    response = f"{new_row}{remove_row}"
    
    return HttpResponse(response)

def agregarFormularioPeriodoCursada(request, id):
    asignatura=Asignatura.objects.get(id=id)
    formulario=PeriodoCursadaForm(instance=asignatura, tipo=asignatura.materia.tipo,  prefix=f'asignatura_{asignatura.pk}')
    return render(request,'cursos/materias/partials/formularioPeriodoCursada.html', {'form':formulario} )