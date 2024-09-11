from django.shortcuts import render
from django.http import HttpResponseBadRequest
from apps.cursos.models import PlanEstudio
from .models import persona
from apps.utils.conversorPalacios import convertirEspecialidad

def get_alumnos_por_especialidad(request):
    plan_de_estudio = request.GET.get('plan_de_estudio')
    
    if not plan_de_estudio:
        return HttpResponseBadRequest("Falta el parámetro 'plan_de_estudio'.")

    try:
        plan_estudio = PlanEstudio.objects.get(id=plan_de_estudio)
        especialidad = convertirEspecialidad(plan_estudio.especialidad)
        orientacion = plan_estudio.orientacion
        print(orientacion, especialidad)
        alumnos = persona.objects.using('id8').filter(especialidad=especialidad)
        print(alumnos)
        context = {
            'alumnos': alumnos
        }

        # Verifica si es una petición HTMX
        if 'HX-Request' in request.headers:
            template = 'parciales/alumnos/alumnosXorientacionXespecialidadXorientacion.html'  # Fragmento HTMX
        else:
            template = 'parciales/alumnos/alumnosXorientacionXespecialidadXorientacion.html'  # Página completa

        return render(request, template, context)

    except PlanEstudio.DoesNotExist:
        return HttpResponseBadRequest("No se encontró el Plan de Estudio.")