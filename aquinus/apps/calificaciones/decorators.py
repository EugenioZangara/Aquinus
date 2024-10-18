from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from aquinus.exceptions import CustomPermissionDenied

from apps.cursos.models import Asignatura, FechasExamenes

def verificar_periodo_curso(view_class):
    print("Verificando periodo de curso...")
    class WrappedView(view_class):
        def dispatch(self, request, *args, **kwargs):
            asignatura_id = kwargs.get('id')
            try:
                asignatura = Asignatura.objects.get(pk=asignatura_id)
                fecha_actual = timezone.now().date()
                anio_asignatura = asignatura.curso.anio
                tipo=asignatura.materia.tipo
                match tipo:
                    case "ANUAL":
                        try:
                            fecha_final=FechasExamenes.objects.get(regimen_materia="ANUAL", subPeriodo="FA",aplica_para=anio_asignatura, anio_lectivo=fecha_actual.year)
                        except FechasExamenes.DoesNotExist:
                            fecha_final=FechasExamenes.objects.get(regimen_materia="ANUAL",subPeriodo="FA", aplica_para="TODOS", anio_lectivo=fecha_actual.year)
                    case "TRIMESTRAL":
                        subPeriodo="FT_"+str(asignatura.periodo_cursado)
                       
                        try:
                            fecha_final=FechasExamenes.objects.get(regimen_materia="TRIMESTRAL", subPeriodo=subPeriodo,aplica_para=anio_asignatura, anio_lectivo=fecha_actual.year)
                        except FechasExamenes.DoesNotExist:
                            fecha_final=FechasExamenes.objects.get(regimen_materia="TRIMESTRAL",subPeriodo=subPeriodo, aplica_para="TODOS", anio_lectivo=fecha_actual.year)
                    case "CUATRIMESTRAL":
                        subPeriodo = "FC_A" if asignatura.periodo_cursado==1 else "FC_B"
                        try:
                            fecha_final=FechasExamenes.objects.get(regimen_materia="CUATRIMESTRAL", subPeriodo=subPeriodo,aplica_para=anio_asignatura, anio_lectivo=fecha_actual.year)
                        except FechasExamenes.DoesNotExist:
                            fecha_final=FechasExamenes.objects.get(regimen_materia="CUATRIMESTRAL",subPeriodo=subPeriodo, aplica_para="TODOS", anio_lectivo=fecha_actual.year)
                if fecha_actual > fecha_final.fechaTopeCalificacion:
                    mensaje = f"El período para ingresar calificaciones de la asignatura {asignatura.materia.nombre} ha finalizado el {fecha_final.fechaTopeCalificacion}."
                    url=reverse_lazy('calificaciones:home')
                    raise CustomPermissionDenied(mensaje, url)
                else:
                    return super().dispatch(request, *args, **kwargs)
                
            except Asignatura.DoesNotExist:
                return redirect('home')
    
    return WrappedView