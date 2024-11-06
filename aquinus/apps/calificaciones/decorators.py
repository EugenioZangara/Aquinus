from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from aquinus.exceptions import CustomPermissionDenied
from django.core.exceptions import ValidationError

from apps.cursos.models import Asignatura, Calificaciones, FechasExamenes

def verificar_periodo_curso(view_class):

    class WrappedView(view_class):
        def dispatch(self, request, *args, **kwargs):
             # Si es una solicitud POST, no hacemos la validación de período
            # if request.method == 'POST':
            #     return super().dispatch(request, *args, **kwargs)
            # Depuramos si se está obteniendo el id correctamente
            asignatura_id = kwargs.get('id') 

            if not asignatura_id:
                return redirect('home')

            try:
                # Intentamos obtener la asignatura
                asignatura = Asignatura.objects.get(pk=asignatura_id)
                fecha_actual = timezone.now().date()
                anio_asignatura = asignatura.curso.anio
                tipo = asignatura.materia.tipo

                # Lógica para obtener la fecha de finalización del período de calificación
                match tipo:
                    case "ANUAL":
                        try:
                            fecha_final = FechasExamenes.objects.get(
                                regimen_materia="ANUAL", subPeriodo="FA", 
                                aplica_para=anio_asignatura, anio_lectivo=fecha_actual.year
                            )
                        except FechasExamenes.DoesNotExist:
                            fecha_final = FechasExamenes.objects.get(
                                regimen_materia="ANUAL", subPeriodo="FA", 
                                aplica_para="TODOS", anio_lectivo=fecha_actual.year
                            )
                    case "TRIMESTRAL":
                        subPeriodo = "FT_" + str(asignatura.periodo_cursado)
                        try:
                            fecha_final = FechasExamenes.objects.get(
                                regimen_materia="TRIMESTRAL", subPeriodo=subPeriodo, 
                                aplica_para=anio_asignatura, anio_lectivo=fecha_actual.year
                            )
                        except FechasExamenes.DoesNotExist:
                            fecha_final = FechasExamenes.objects.get(
                                regimen_materia="TRIMESTRAL", subPeriodo=subPeriodo, 
                                aplica_para="TODOS", anio_lectivo=fecha_actual.year
                            )
                    case "CUATRIMESTRAL":
                        subPeriodo = "FC_A" if asignatura.periodo_cursado == 1 else "FC_B"
                        try:
                            fecha_final = FechasExamenes.objects.get(
                                regimen_materia="CUATRIMESTRAL", subPeriodo=subPeriodo, 
                                aplica_para=anio_asignatura, anio_lectivo=fecha_actual.year
                            )
                        except FechasExamenes.DoesNotExist:
                            fecha_final = FechasExamenes.objects.get(
                                regimen_materia="CUATRIMESTRAL", subPeriodo=subPeriodo, 
                                aplica_para="TODOS", anio_lectivo=fecha_actual.year
                            )

                if fecha_actual > fecha_final.fechaTopeCalificacion:
                    mensaje = f"El período para ingresar calificaciones de la asignatura {asignatura.materia.nombre} ha finalizado el {fecha_final.fechaTopeCalificacion}."
                    url = reverse_lazy('calificaciones:home')
                    raise CustomPermissionDenied(mensaje, url) 
                    # Agregar un indicador al contexto de que el periodo ha terminado
                elif fecha_actual > fecha_final.fechaInicioCalificacion and fecha_actual < fecha_final.fechaTopeCalificacion:
                    request.alerta_periodo_finalizado = True
                else:
                    request.alerta_periodo_finalizado = False

                return super().dispatch(request, *args, **kwargs)
            except Asignatura.DoesNotExist:  
                return redirect('home')
            except ValidationError:
                print("Error de validación")

    return WrappedView
