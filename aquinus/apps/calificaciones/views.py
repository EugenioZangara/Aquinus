from datetime import date
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.cursos.models import Asignatura, Cursante, Calificaciones, FechasExamenes
from django.db.models import Count, Avg
import statistics
from django.core.exceptions import ValidationError

from django.forms import  modelformset_factory
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.calificaciones.decorators import verificar_periodo_curso
from .utils import periodoMateria
from apps.alumnos.models import persona
from .forms import CalificacionesForm
from .tasks import calcular_promedios_periodo
# Create your views here.

class HomeCalificaciones(TemplateView):
    template_name="calificaciones/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calcular_promedios_periodo()
        perfil_usuario=self.request.user.perfil
        asignaturas=Asignatura.objects.filter(profesor=perfil_usuario).all().order_by('materia')
        asignaturas_con_alumnos={}
        for asignatura in asignaturas:
            cantidad_alumnos_por_curso = Cursante.objects.filter(curso=asignatura.curso).aggregate(total=Count('id'))['total']
            asignaturas_con_alumnos[asignatura]=cantidad_alumnos_por_curso
            
            
        context["asignaturas_con_alumnos"] = asignaturas_con_alumnos
        context['active_tab']="calificaciones"
        return context
    
    
def getFechasPeriodoCursada(periodo,tipo, anio):
    """
    Filtro que devuelve las fechas de los períodos de las materias.
    
    """
    anio_lectivo=date.today().year
    if tipo=="ANUAL" or tipo=="TRIMESTRAL":
        try:
            trimestre1=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="T1", aplica_para=anio, anio_lectivo=anio_lectivo)
            trimestre2=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="T2", aplica_para=anio, anio_lectivo=anio_lectivo)
            trimestre3=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="T3", aplica_para=anio, anio_lectivo=anio_lectivo)
            
        except FechasExamenes.DoesNotExist:
            trimestre1=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="T1", aplica_para="TODOS", anio_lectivo=anio_lectivo)
            trimestre2=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="T2", aplica_para="TODOS", anio_lectivo=anio_lectivo)
            trimestre3=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="T3", aplica_para="TODOS", anio_lectivo=anio_lectivo)
        trimestres=[trimestre1,trimestre2,trimestre3]
        
    elif tipo=="CUATRIMESTRAL":
        try:
            bimestre1_A=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B1_A", aplica_para=anio, anio_lectivo=anio_lectivo)
            bimestre2_A=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B2_A", aplica_para=anio, anio_lectivo=anio_lectivo)
            bimestre1_B=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B1_B", aplica_para=anio, anio_lectivo=anio_lectivo)
            bimestre2_B=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B2_B", aplica_para=anio, anio_lectivo=anio_lectivo)
        except:
            bimestre1_A=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B1_A", aplica_para="TODOS", anio_lectivo=anio_lectivo)
            bimestre2_A=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B2_A", aplica_para="TODOS", anio_lectivo=anio_lectivo)
            bimestre1_B=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B1_B", aplica_para="TODOS", anio_lectivo=anio_lectivo)
            bimestre2_B=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="B2_B", aplica_para="TODOS", anio_lectivo=anio_lectivo)
            
        cuatrimestre1=[bimestre1_A, bimestre1_B, bimestre2_A, bimestre2_B]
        cuatrimestre2=[bimestre1_A, bimestre1_B, bimestre2_A, bimestre2_B]


    if periodo: 
        hoy = date.today()       
        match tipo:
            case "ANUAL":
                try:
                    finales=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="FA", aplica_para=anio, anio_lectivo=anio_lectivo)
                except FechasExamenes.DoesNotExist:
                    finales=FechasExamenes.objects.get(regimen_materia=tipo,subPeriodo="FA", aplica_para="TODOS", anio_lectivo=anio_lectivo)
    
                for trimestre in trimestres:
                    if hoy>=trimestre.fechaInicioCalificacion and hoy<=trimestre.fechaTopeCalificacion:
                        return trimestre.fechaInicioCalificacion ,trimestre.fechaTopeCalificacion
                if hoy>=finales.fechaInicioCalificacion and hoy<=finales.fechaTopeCalificacion:
                    return finales.fechaInicioCalificacion,finales.fechaTopeCalificacion
                
            case "CUATRIMESTRAL":
                if periodo in("Primer Bimestre - 1er. Cuatrimestre","Cierre Primer Cuatrimestre","Final Primer Cuatrimestre"):
                    try:
                        fechas_finales_cuatrimestre1=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FC_A", aplica_para=anio, anio_lectivo=anio_lectivo)
                    except:
                        fechas_finales_cuatrimestre1=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FC_A", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                    for bimestre in cuatrimestre1:
                        if hoy>=bimestre.fechaInicioCalificacion and hoy<=bimestre.fechaTopeCalificacion:
                            return bimestre.fechaInicioCalificacion, bimestre.fechaTopeCalificacion
                    if hoy>=fechas_finales_cuatrimestre1.fechaInicioCalificacion and hoy<=fechas_finales_cuatrimestre1.fechaTopeCalificacion:
                        return fechas_finales_cuatrimestre1.fechaInicioCalificacion, fechas_finales_cuatrimestre1.fechaTopeCalificacion
                if periodo in("Primer Bimestre - 2do. Cuatrimestre","Cierre Segundo Cuatrimestre","Final Segundo Cuatrimestre"):
                    try:
                        fechas_finales_cuatrimestre1=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FC_B", aplica_para=anio, anio_lectivo=anio_lectivo)
                    except:
                        fechas_finales_cuatrimestre1=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FC_B", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                    for bimestre in cuatrimestre1:
                        if hoy>=bimestre.fechaInicioCalificacion and hoy<=bimestre.fechaTopeCalificacion:
                            return bimestre.fechaInicioCalificacion, bimestre.fechaTopeCalificacion
                    if hoy>=fechas_finales_cuatrimestre1.fechaInicioCalificacion and hoy<=fechas_finales_cuatrimestre1.fechaTopeCalificacion:
                        return fechas_finales_cuatrimestre1.fechaInicioCalificacion, fechas_finales_cuatrimestre1.fechaTopeCalificacion   
                
            
                    
            case "SEMESTRAL":
                match periodo:
                    case "Primer Semestre":
                        try:
                            finales_semestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FS_1", aplica_para=anio, anio_lectivo=anio_lectivo)
                        except:
                            finales_semestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FS_1", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                        if hoy>=trimestre1.fechaInicioCalificacion and hoy<=trimestre1.fechaTopeCalificacion:
                            return trimestre1.fechaInicioCalificacion, trimestre1.fechaTopeCalificacion
                        if hoy>=trimestre2.fechaInicioCalificacion and hoy<=trimestre2.fechaTopeCalificacion:
                            return trimestre2.fechaInicioCalificacion, trimestre2.fechaTopeCalificacion
                        if hoy>=finales_semestrales.fechaInicioCalificacion and hoy<=finales_semestrales.fechaTopeCalificacion:
                            return finales_semestrales.fechaInicioCalificacion, finales_semestrales.fechaTopeCalificacion
                    case "Segundo Semestre":
                        try:
                            finales_semestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FS_2", aplica_para=anio, anio_lectivo=anio_lectivo)
                        except:
                            finales_semestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FS_2", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                        if hoy>=trimestre3.fechaInicioCalificacion and hoy<=trimestre3.fechaTopeCalificacion:
                            return trimestre3.fechaInicioCalificacion, trimestre3.fechaTopeCalificacion
                        if hoy>=trimestre2.fechaInicioCalificacion and hoy<=trimestre2.fechaTopeCalificacion:
                            return trimestre2.fechaInicioCalificacion, trimestre2.fechaTopeCalificacion
                        if hoy>=finales_semestrales.fechaInicioCalificacion and hoy<=finales_semestrales.fechaTopeCalificacion:
                            return finales_semestrales.fechaInicioCalificacion, finales_semestrales.fechaTopeCalificacion
                                                 
            case "TRIMESTRAL":
                match periodo:
                    case "Primer Trimestre":
                        try:
                            finales_trimestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FT_1", aplica_para=anio, anio_lectivo=anio_lectivo)
                        except:
                            finales_trimestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FT_1", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                        if hoy>=trimestre1.fechaInicioCalificacion and hoy<=trimestre1.fechaTopeCalificacion:
                            return trimestre1.fechaInicioCalificacion, trimestre1.fechaTopeCalificacion
                        if hoy>=finales_trimestrales.fechaInicioCalificacion and hoy<=finales_trimestrales.fechaTopeCalificacion:
                            return finales_trimestrales.fechaInicioCalificacion, finales_trimestrales.fechaTopeCalificacion
                        else:
                            return "error en el cálculo de las fechas del trimestre"
                    case "Segundo Trimestre":
                        try:
                            finales_trimestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FT_2", aplica_para=anio, anio_lectivo=anio_lectivo)
                        except:
                            finales_trimestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FT_2", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                        if hoy>=trimestre2.fechaInicioCalificacion and hoy<=trimestre2.fechaTopeCalificacion:
                            return trimestre2.fechaInicioCalificacion, trimestre2.fechaTopeCalificacion
                        if hoy>=finales_trimestrales.fechaInicioCalificacion and hoy<=finales_trimestrales.fechaTopeCalificacion:
                            return finales_trimestrales.fechaInicioCalificacion, finales_trimestrales.fechaTopeCalificacion
                        else:
                            return "error en el cálculo de las fechas del trimestre"
                    case "Tercer Trimestre":
                        try:
                            finales_trimestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FT_3", aplica_para=anio, anio_lectivo=anio_lectivo)
                        except:
                            finales_trimestrales=FechasExamenes.objects.get(regimen_materia=tipo, subPeriodo="FT_3", aplica_para="TODOS", anio_lectivo=anio_lectivo)
                        if hoy>=trimestre3.fechaInicioCalificacion and hoy<=trimestre3.fechaTopeCalificacion:
                            return trimestre3.fechaInicioCalificacion, trimestre3.fechaTopeCalificacion
                        if hoy>=finales_trimestrales.fechaInicioCalificacion and hoy<=finales_trimestrales.fechaTopeCalificacion:
                            return finales_trimestrales.fechaInicioCalificacion, finales_trimestrales.fechaTopeCalificacion
                        else:
                            return "error en el cálculo de las fechas del trimestre"
     
            case _:

                return "Desconocido"
    else:
        if tipo=="ANUAL":
            return "No aplica"
        else:
            return "SIN ASIGNAR"
        
        
@verificar_periodo_curso
class CalificarView(TemplateView):
    template_name = "calificaciones/calificar.html"
    success_url = 'calificaciones:home'
    
    def get_asignatura(self):
        return get_object_or_404(Asignatura, id=self.kwargs['id'])
    
    def get_alumnos(self, asignatura):
        dni_cursantes = list(Cursante.objects.filter(curso=asignatura.curso).values_list('dni', flat=True))
        return persona.objects.filter(dni__in=dni_cursantes).using('id8')
    
    def get_formset(self, data=None):
    
        asignatura = self.get_asignatura()
        alumnos = self.get_alumnos(asignatura)
        CalificacionFormSet = modelformset_factory(Calificaciones, form=CalificacionesForm, extra=len(alumnos))
        queryset = Calificaciones.objects.none()
        # Obtener las fechas del periodo de calificación para la asignatura
        fechasPeriodoCalificacion = getFechasPeriodoCursada(
            periodoMateria(asignatura), 
            asignatura.materia.tipo, 
            asignatura.materia.anio
        )

        return CalificacionFormSet(data, queryset=queryset, form_kwargs={'fechas_periodo': fechasPeriodoCalificacion} ), alumnos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura = self.get_asignatura()
        periodoCalificacion = periodoMateria(asignatura)

        formset, alumnos = self.get_formset()
        forms_and_alumnos = zip(formset, alumnos)
        context['alerta_periodo_finalizado'] = getattr(self.request, 'alerta_periodo_finalizado', False)
        context["periodoCalificacion"] = periodoCalificacion
        context['fechasPeriodoCalificacion'] =getFechasPeriodoCursada(periodoCalificacion,asignatura.materia.tipo, asignatura.materia.anio)
        context["asignatura"] = asignatura
        context["forms_and_alumnos"] = forms_and_alumnos
        context["formset"] = formset  # Agregamos el formset al contexto
        context['active_tab']="calificaciones"

        return context
    
    def post(self, request, *args, **kwargs):    
        asignatura = self.get_asignatura()
          # Obtener las fechas del periodo de calificación para la asignatura
        fechasPeriodoCalificacion = getFechasPeriodoCursada(
            periodoMateria(asignatura), 
            asignatura.materia.tipo, 
            asignatura.materia.anio
        )       
        CalificacionFormSet = modelformset_factory(Calificaciones, form=CalificacionesForm, extra=len(self.get_alumnos(asignatura)))
        queryset = Calificaciones.objects.none()
        formset = CalificacionFormSet(request.POST, queryset=queryset, form_kwargs={'fechas_periodo': fechasPeriodoCalificacion})
        alumnos = self.get_alumnos(asignatura)
        
        perfil_usuario=self.request.user.perfil
        if perfil_usuario.puede_calificar==False:
            messages.error(request, f'No tiene permisos para calificar.')
            return redirect(self.success_url)
        else:
            
            if formset.is_valid():
             
                tipo="FINAL" if request.alerta_periodo_finalizado else "ORDINARIA"
                instances = formset.save(commit=False)
             
                for instance, alumno in zip(instances, alumnos):
                    if instance.valor is not None:
                        cursante=Cursante.objects.get(dni=alumno.dni)
                        instance.cursante = cursante
                        instance.asignatura = asignatura
                        instance.valor = instance.valor
                        instance.tipo=tipo
                        instance.calificador=self.request.user.perfil
                        # Ejecuta la validación antes de guardar
                        try:
                            instance.validate_unique_calification()
                            instance.save()
                            messages.success(request, f'Calificaciones para cargadas correctamente para el alumnos {cursante}.')
                        except ValidationError as e:
                            messages.error(request, f'Error al guardar la calificación del alumno {cursante}: {e}')
                        
                return redirect(self.success_url)
            else:
               
                print("Errores en el formset:", formset.errors)
                for form in formset:
                    print("Error en el form individual:", form.errors)
                messages.error(request, f'Error al cargar las calificaciones.')
                # Si el formset no es válido, mostrar el formulario nuevamente
                return self.render_to_response(self.get_context_data(formset=formset))


def obtenerCalificacionesAnual(asignatura, alumno):
    calificaciones = Calificaciones.objects.filter(asignatura=asignatura, cursante__dni=alumno.dni)
    #OBTENEMOS FECHAS PARA CADA SUBPERIODO DE LAS MATERIAS ANUALES
    try:
        primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T1", aplica_para=asignatura.materia.anio)
        segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para=asignatura.materia.anio)
        tercer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T3", aplica_para=asignatura.materia.anio)
        fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FA", aplica_para=asignatura.materia.anio)
    except FechasExamenes.DoesNotExist:
        primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T1", aplica_para="TODOS")
        segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para="TODOS")
        tercer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T3", aplica_para="TODOS")
        fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FA", aplica_para="TODOS")

    #OBTENES LAS CALIFICACIONES DE CADA TRIMESTRE EN FUNCIÓN DE LAS FECHAS OBTENIDAS ANTES
    calificaciones_1T=calificaciones.filter(fecha_examen__gte=primer_trimestre.fechaInicioCalificacion, fecha_examen__lte=primer_trimestre.fechaTopeCalificacion)  
    calificaciones_2T=calificaciones.filter(fecha_examen__gte=segundo_trimestre.fechaInicioCalificacion, fecha_examen__lte=segundo_trimestre.fechaTopeCalificacion)
    calificaciones_3T=calificaciones.filter(fecha_examen__gte=tercer_trimestre.fechaInicioCalificacion, fecha_examen__lte=tercer_trimestre.fechaTopeCalificacion)
    # Extraer los promedios de los diccionarios resultantes
    # Agregar el promedio y extraer el valor
    promedio_1T = round(calificaciones_1T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
    promedio_2T = round(calificaciones_2T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
    promedio_3T = round(calificaciones_3T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)


    # Calcular el promedio de la cursada
    promedio_cursada = round(statistics.mean([promedio_1T , promedio_2T , promedio_3T]),2)
    try:
        calificacion_examen_final=calificaciones.get(tipo="FINAL")
        calificacion_final=round(statistics.mean([calificacion_examen_final.valor,promedio_cursada]),2)
    except Calificaciones.DoesNotExist:
        calificacion_final="N/A"
        calificacion_examen_final={"valor":"Sin Calificación"}
        
    calificaciones_anuales={'primer_trimestre':calificaciones_1T,'promedio_1T':promedio_1T, 'segundo_trimestre':calificaciones_2T,'promedio_2T':promedio_2T, 'tercer_trimestre':calificaciones_3T, 'promedio_3T':promedio_3T,'promedio_cursada':promedio_cursada, "examen_final":calificacion_examen_final,"calificacion_final":calificacion_final }
    return calificaciones_anuales


def obtenerCalificacionesCuatrimestral(asignatura, alumno):
    calificaciones = Calificaciones.objects.filter(asignatura=asignatura, cursante__dni=alumno.dni)
    #OBTENEMOS FECHAS PARA CADA SUBPERIODO DE LAS MATERIAS ANUALES
    try:
        if asignatura.periodo_cursado==1:
            primer_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B1_A", aplica_para=asignatura.materia.anio)
            segundo_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B2_A", aplica_para=asignatura.materia.anio)
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FC_A", aplica_para=asignatura.materia.anio)
        else:
            primer_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B1_B", aplica_para=asignatura.materia.anio)
            segundo_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B2_B", aplica_para=asignatura.materia.anio)
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FC_B", aplica_para=asignatura.materia.anio)
    except FechasExamenes.DoesNotExist:
        if asignatura.periodo_cursado==1:
            primer_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B1_A", aplica_para="TODOS")
            segundo_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B2_A", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FC_A", aplica_para="TODOS")
        else:
            primer_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B1_B", aplica_para="TODOS")
            segundo_bimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="B2_B", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FC_B", aplica_para="TODOS")
 
     #OBTENES LAS CALIFICACIONES DE CADA TRIMESTRE EN FUNCIÓN DE LAS FECHAS OBTENIDAS ANTES
    calificaciones_1B=calificaciones.filter(fecha_examen__gte=primer_bimestre.fechaInicioCalificacion, fecha_examen__lte=primer_bimestre.fechaTopeCalificacion)  
    calificaciones_2B=calificaciones.filter(fecha_examen__gte=segundo_bimestre.fechaInicioCalificacion, fecha_examen__lte=segundo_bimestre.fechaTopeCalificacion)
   
    # Extraer los promedios de los diccionarios resultantes
    # Agregar el promedio y extraer el valor
    promedio_1B = round(calificaciones_1B.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
    promedio_2B = round(calificaciones_2B.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
    
     # Calcular el promedio de la cursada
    promedio_cursada = round(statistics.mean([promedio_1B , promedio_2B ]))
    
    try:
        calificacion_examen_final=calificaciones.get(tipo="FINAL")
        calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_cursada])
    except Calificaciones.DoesNotExist:
        calificacion_final="N/A"
        calificacion_examen_final="Sin Calificación"
        
    calificaciones_semestrales={'primer_bimestre':calificaciones_1B,'promedio_1B':promedio_1B, 'segundo_bimestre':calificaciones_2B,'promedio_2B':promedio_2B,  'promedio_cursada':promedio_cursada, "examen_final":calificacion_examen_final,"calificacion_final":calificacion_final }
    return calificaciones_semestrales    
            
def obtenerCalificacionesSemestral(asignatura, alumno):
    calificaciones = Calificaciones.objects.filter(asignatura=asignatura, cursante__dni=alumno.dni)
 
    #OBTENEMOS FECHAS PARA CADA SUBPERIODO DE LAS MATERIAS ANUALES
    try:
        # Asumimos que la fecha de los finales semestrales, se corresponden con la del trimestre correspondiente
        if asignatura.periodo_cursado==1:
            primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T1", aplica_para=asignatura.materia.anio)
            segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para=asignatura.materia.anio)
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia="TRIMESTRAL", subPeriodo="FT_2", aplica_para=asignatura.materia.anio) 
        else:
            primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para=asignatura.materia.anio)
            segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T3", aplica_para=asignatura.materia.anio)
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia="TRIMESTRAL", subPeriodo="FT_3", aplica_para=asignatura.materia.anio)
    except FechasExamenes.DoesNotExist:
        if asignatura.periodo_cursado==1:
            primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T1", aplica_para="TODOS")
            segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia="TRIMESTRAL", subPeriodo="FT_2", aplica_para="TODOS")
        else:
            primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para="TODOS")
            segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T3", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia="TRIMESTRAL", subPeriodo="FT_3", aplica_para="TODOS")
    #OBTENES LAS CALIFICACIONES DE CADA TRIMESTRE EN FUNCIÓN DE LAS FECHAS OBTENIDAS ANTES
    calificaciones_1T=calificaciones.filter(fecha_examen__gte=primer_trimestre.fechaInicioCalificacion, fecha_examen__lte=primer_trimestre.fechaTopeCalificacion)  
    calificaciones_2T=calificaciones.filter(fecha_examen__gte=segundo_trimestre.fechaInicioCalificacion, fecha_examen__lte=segundo_trimestre.fechaTopeCalificacion)
   
    # Extraer los promedios de los diccionarios resultantes
    # Agregar el promedio y extraer el valor
    promedio_1T = round(calificaciones_1T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
    promedio_2T = round(calificaciones_2T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
    
     # Calcular el promedio de la cursada
    promedio_cursada = round(statistics.mean([promedio_1T , promedio_2T ]))
    try:
        calificacion_examen_final=calificaciones.get(tipo="FINAL")
        calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_cursada])
    except Calificaciones.DoesNotExist:
        calificacion_final="N/A"
        calificacion_examen_final={"valor":"Sin Calificación"}
        
    calificaciones_semestrales={'primer_trimestre':calificaciones_1T,'promedio_1T':promedio_1T, 'segundo_trimestre':calificaciones_2T,'promedio_2T':promedio_2T,  'promedio_cursada':promedio_cursada, "examen_final":calificacion_examen_final,"calificacion_final":calificacion_final }
    return calificaciones_semestrales



def obtenerCalificacionesTrimestral(asignatura, alumno):
    calificaciones = Calificaciones.objects.filter(asignatura=asignatura, cursante__dni=alumno.dni)
    #OBTENEMOS FECHAS PARA CADA SUBPERIODO DE LAS MATERIAS ANUALES
    
    try:
        if asignatura.periodo_cursado==1:
            primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T1", aplica_para=asignatura.materia.anio)
             
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FT_1", aplica_para=asignatura.materia.anio)
            calificaciones_T=calificaciones.filter(fecha_examen__gte=primer_trimestre.fechaInicioCalificacion, fecha_examen__lte=primer_trimestre.fechaTopeCalificacion)
            
            promedio_T = round(calificaciones_T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
            try:
                
                calificacion_examen_final=calificaciones.get(tipo="FINAL")
                calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_T])
            except Calificaciones.DoesNotExist:
                calificacion_final="N/A"
                calificacion_examen_final={"valor":"Sin Calificación"} 
        elif asignatura.periodo_cursado==2:
            segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para=asignatura.materia.anio)
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FT_2", aplica_para=asignatura.materia.anio)
            calificaciones_T=calificaciones.filter(fecha_examen__gte=segundo_trimestre.fechaInicioCalificacion, fecha_examen__lte=segundo_trimestre.fechaTopeCalificacion)
            promedio_T = round(calificaciones_T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
            try:
                
                calificacion_examen_final=calificaciones.get(tipo="FINAL")
                calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_T])
            except Calificaciones.DoesNotExist:
                calificacion_final="N/A"
                calificacion_examen_final={"valor":"Sin Calificación"}

        else:
            tercer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T3", aplica_para=asignatura.materia.anio)
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FT_3", aplica_para=asignatura.materia.anio)
            calificaciones_T=calificaciones.filter(fecha_examen__gte=tercer_trimestre.fechaInicioCalificacion, fecha_examen__lte=tercer_trimestre.fechaTopeCalificacion)
            promedio_T = round(calificaciones_T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
            try:
                
                calificacion_examen_final=calificaciones.get(tipo="FINAL")
                calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_T])
            except Calificaciones.DoesNotExist:
                calificacion_final="N/A"
                calificacion_examen_final={"valor":"Sin Calificación"}
            
    except FechasExamenes.DoesNotExist:
        if asignatura.periodo_cursado==1:
            primer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T1", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FT_1", aplica_para="TODOS")
            calificaciones_T=calificaciones.filter(fecha_examen__gte=primer_trimestre.fechaInicioCalificacion, fecha_examen__lte=primer_trimestre.fechaTopeCalificacion) 
            promedio_T = round(calificaciones_T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
            
            try:
                
                calificacion_examen_final=calificaciones.get(fecha_examen__gte=primer_trimestre.fechaTopeCalificacion, fecha_examen__lte=fechas_examen_final.fechaTopeCalificacion)
                calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_T])
            except Calificaciones.DoesNotExist:
                calificacion_final="N/A"
                calificacion_examen_final={"valor":"Sin Calificación"}
        elif asignatura.periodo_cursado==2:
            segundo_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T2", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FT_2", aplica_para="TODOS")
            calificaciones_T=calificaciones.filter(fecha_examen__gte=segundo_trimestre.fechaInicioCalificacion, fecha_examen__lte=segundo_trimestre.fechaTopeCalificacion)
            promedio_T = round(calificaciones_T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
            try:
                
                calificacion_examen_final=calificaciones.get(fecha_examen__gte=segundo_trimestre.fechaTopeCalificacion, fecha_examen__lte=fechas_examen_final.fechaTopeCalificacion)
                calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_T])
            except Calificaciones.DoesNotExist:
                calificacion_final="N/A"
                calificacion_examen_final={"valor":"Sin Calificación"}
        else:
            tercer_trimestre=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="T3", aplica_para="TODOS")
            fechas_examen_final=FechasExamenes.objects.get( regimen_materia=asignatura.materia.tipo, subPeriodo="FT_3", aplica_para="TODOS")
            calificaciones_T=calificaciones.filter(fecha_examen__gte=tercer_trimestre.fechaInicioCalificacion, fecha_examen__lte=tercer_trimestre.fechaTopeCalificacion)
            promedio_T = round(calificaciones_T.aggregate(promedio=Avg('valor'))['promedio'] or 0, 2)
            try:
                
                calificacion_examen_final=calificaciones.get(fecha_examen__gte=tercer_trimestre.fechaTopeCalificacion, fecha_examen__lte=fechas_examen_final.fechaTopeCalificacion)
                calificacion_final=statistics.mean([calificacion_examen_final.valor,promedio_T])
            except Calificaciones.DoesNotExist:
                calificacion_final="N/A"
                calificacion_examen_final={"valor":"Sin Calificación"}
   

    
        
    calificaciones_trimestral={'calificaciones_trimestre':calificaciones_T,'promedio_T':promedio_T,  "examen_final":calificacion_examen_final,"calificacion_final":calificacion_final }
    return calificaciones_trimestral


class CalificacionesAsignatura(TemplateView):
    template_name = "calificaciones/asignatura.html"
    success_url = 'calificaciones:home'

    def get_asignatura(self):
        return get_object_or_404(Asignatura, id=self.kwargs['id'])

    def get_alumnos(self, asignatura):
        dni_cursantes = list(Cursante.objects.filter(curso=asignatura.curso).values_list('dni', flat=True))
        return persona.objects.filter(dni__in=dni_cursantes).using('id8')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura=self.get_asignatura()
        alumnos=self.get_alumnos(asignatura)
        alumnos_calificaciones={}
        for alumno in alumnos:
            if asignatura.materia.tipo=="ANUAL":
                calificaciones=obtenerCalificacionesAnual(asignatura, alumno)
            elif asignatura.materia.tipo=="CUATRIMESTRAL":
                calificaciones=obtenerCalificacionesCuatrimestral(asignatura, alumno)
            elif asignatura.materia.tipo=="SEMESTRAL":
                calificaciones=obtenerCalificacionesSemestral(asignatura, alumno)
            elif asignatura.materia.tipo=="TRIMESTRAL":
                calificaciones=obtenerCalificacionesTrimestral(asignatura, alumno)
            alumnos_calificaciones[alumno]=calificaciones
            
        
        curso=asignatura.curso
        context['curso']=curso
        context['alumnos']=alumnos
        context['asignatura']=asignatura
        context['alumnos_calificaciones']=alumnos_calificaciones

        return context
    
class BoletinView(TemplateView):
    template_name = "calificaciones/boletin.html"
    
    def get_alumno(self):
        alumno = get_object_or_404(persona.objects.using('id8'), dni=self.kwargs['dni'])
        return alumno
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materias_con_calificaciones_anuales={}
        materias_con_calificaciones_cuatrimestrales={}
        materias_con_calificaciones_semestrales={}
        materias_con_calificaciones_trimestrales={}
        alumno=self.get_alumno()
        cursante=Cursante.objects.get(dni=alumno.dni)
     
        asignaturas_anuales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="ANUAL")
        #calificaciones_anuales=Calificaciones.objects.filter(cursante=cursante, asignatura__in=asignaturas_anuales)
        for asignatura in asignaturas_anuales:
            materias_con_calificaciones_anuales[asignatura]=obtenerCalificacionesAnual(asignatura, alumno)
       
        asignaturas_semestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="SEMESTRAL")
        for asignatura in asignaturas_semestrales:
            materias_con_calificaciones_semestrales[asignatura]=obtenerCalificacionesSemestral(asignatura, alumno)
            
        asignaturas_cuatrimestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="CUATRIMESTRAL")
        for asignatura in asignaturas_cuatrimestrales:
            materias_con_calificaciones_cuatrimestrales[asignatura]=obtenerCalificacionesCuatrimestral(asignatura, alumno)
            
        asignaturas_trimestrales=Asignatura.objects.filter(curso=cursante.curso, materia__tipo="TRIMESTRAL")   
        for asignatura in asignaturas_trimestrales:
            materias_con_calificaciones_trimestrales[asignatura]=obtenerCalificacionesTrimestral(asignatura, alumno)
            
            
        context['materias_con_calificaciones_anuales']=materias_con_calificaciones_anuales
        context['materias_con_calificaciones_cuatrimestrales']=materias_con_calificaciones_cuatrimestrales
        context['materias_con_calificaciones_trimestrales']=materias_con_calificaciones_trimestrales
        context['materias_con_calificaciones_semestrales']=materias_con_calificaciones_semestrales       
        context['materias_con_calificaciones']=materias_con_calificaciones_anuales
        context['alumno']=alumno
        context['asignaturas_anuales']=asignaturas_anuales
        #context['calificaciones']=calificaciones_anuales
        
        return context