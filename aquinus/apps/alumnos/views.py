from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.db.models import Q
from apps.cursos.models import PlanEstudio
from .models import persona
from apps.utils.conversorPalacios import convertirEspecialidad, convertirOrientaciones
from apps.cursos.models import Cursante

def get_alumnos_por_especialidad(request):
    plan_de_estudio = request.GET.get('plan_de_estudio')
    anio=request.GET.get('anio') or None
    buscar = request.GET.get('search', '').strip()  # Recupera el valor del input
    template='parciales/alumnos/alumnosXorientacionXespecialidadXorientacion.html'
    
    if not plan_de_estudio:
        return HttpResponseBadRequest("Falta el parámetro 'plan_de_estudio'.")

    try:
        plan_estudio = PlanEstudio.objects.get(id=plan_de_estudio)
        especialidad = convertirEspecialidad(plan_estudio.especialidad) or ''
        orientacion = convertirOrientaciones(plan_estudio.orientacion) or ''  
        print(especialidad, orientacion, "ESPECIALIDAD Y ORIENTACIÓN PARA LA QUERY")    
        alumnos_con_curso_asignado=Cursante.objects.filter(activo=True).values_list('dni', flat=True)
        if anio=="0":
            
            if buscar:
                print("BUSCA ESTA ESPECIALIDAD, ORIENTACION:  ", especialidad, orientacion  )
                # Filtrar por especialidad, grado y orientación, además de los campos de búsqueda
                alumnos = persona.objects.using('id8').filter(
                    especialidad=especialidad,
                    
                    orientacion=orientacion,
                    estado=1
                ).filter(
                    Q(apellidos__icontains=buscar) |
                    Q(nombres__icontains=buscar) |
                    Q(dni__icontains=buscar)
                ).exclude(
                    dni__in=list(alumnos_con_curso_asignado)
                ).order_by('apellidos')
            else:
                

                # Si no hay búsqueda, solo aplica los otros filtros
                alumnos = persona.objects.using('id8').filter(
                    especialidad=especialidad,

                    orientacion=orientacion,
                       estado=1
                ).exclude(
                    dni__in=list(alumnos_con_curso_asignado)
                ).order_by('apellidos')
             
        else:
            print("BUSCA ESTA ESPECIALIDAD, ORIENTACION:  ", especialidad, orientacion  )
            alumnos = persona.objects.using('id8').filter(especialidad=especialidad, orientacion=orientacion, grado=anio,  estado=1).order_by('apellidos').exclude(dni__in=list(alumnos_con_curso_asignado))
 
           
        context = {
            'alumnos': alumnos
        }
     
        # Verifica si es una petición HTMX
        if 'HX-Request' in request.headers:
            if anio!="0":
                template = template  # Fragmento HTMX
            else:
                template='parciales/alumnos/alumnosTodosAnios.html'
        else:
            template = 'parciales/alumnos/alumnosXorientacionXespecialidadXorientacion.html'  # Página completa

        return render(request, template, context)

    except PlanEstudio.DoesNotExist:
        return HttpResponseBadRequest("No se encontró el Plan de Estudio.")
    
    

    