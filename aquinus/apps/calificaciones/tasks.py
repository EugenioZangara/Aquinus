from celery import shared_task
from django.db.models import Avg
from django.db.models.functions import Round
from django.contrib import messages
from django.core.exceptions import ValidationError

from django.db import transaction
from django.utils import timezone
from apps.cursos.models import  Cursante, FechasExamenes, Calificaciones, Asignatura

equivalencia_periodos={
    "T1":1,
    "T2":2,
    "T3":3,
    "B1_A":1,
    "B2_A":2,
    "B1_B":1,
    "B2_B":2,
    
}
equivalencia_tipo_calificacion={
    "T1":"TRIMESTRAL_1",
    "T2":"TRIMESTRAL_2",
    "T3":"TRIMESTRAL_3",
    "B1_A":"BIMESTRAL_1",
    "B2_A":"BIMESTRAL_2",
    "B1_B":"BIMESTRAL_1",
    "B2_B":"BIMESTRAL_2",

}

@shared_task
def calcular_promedios_periodo():
    # Obtener la fecha actual
    fecha_hoy = timezone.now().date()
    periodos_promediables=["T1","T2","T3","B1_A","B2_A","B1_B","B2_B"]

    # Filtrar los periodos que terminan hoy
    periodos_cerrados = FechasExamenes.objects.filter(fechaTopeCalificacion='2024-10-30')
   
    with transaction.atomic():  # Inicia la transacción
        for periodo in periodos_cerrados:
            
            if periodo.subPeriodo in periodos_promediables:
            # Obtener el régimen de la materia
                regimen_materia = periodo.regimen_materia
                fecha_inicio = periodo.fechaInicioCalificacion
                fecha_fin = periodo.fechaTopeCalificacion
                subperiodo = equivalencia_periodos[periodo.subPeriodo]
                aplica_para=periodo.aplica_para
                
                # Filtrar calificaciones en el rango de fechas
                asignaturas=Asignatura.objects.filter(materia__tipo=regimen_materia, periodo_cursado=subperiodo, materia__anio=aplica_para)
                calificaciones = Calificaciones.objects.filter(fecha_examen__range=(fecha_inicio, fecha_fin), asignatura__in=asignaturas).values('cursante', 'asignatura').annotate(promedio=Round(Avg('valor'), 2))
                
                # Crear nuevas instancias de calificación para cada cursante y asignatura
                for calificacion in calificaciones:
                    print(periodo.regimen_materia)
                    if periodo.regimen_materia=="ANUAL":
                        print("entro en anual")
                        nueva_calificacion = Calificaciones(
                            cursante=Cursante.objects.get(id=calificacion['cursante']),
                            asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                            valor=calificacion['promedio'],
                            tipo=equivalencia_tipo_calificacion[periodo.subPeriodo],  
                            fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                            # Agrega otros campos necesarios según tu modelo
                        )
                        nueva_calificacion.save()  # Se guardará como parte de la transacción
                        
                        #Si es el último timestre agregamos la calificación de promedio cursada
                        if periodo.subPeriodo=="T3":
                            try:
                                calificacion_primer_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="TRIMESTRAL_1").first()
                                calificacion_segundo_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="TRIMESTRAL_2").first()
                                calificacion_tercer_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="TRIMESTRAL_3").first()  
                                promedio=Avg([calificacion_primer_trimestre.valor, calificacion_segundo_trimestre.valor, calificacion_tercer_trimestre.valor])
                                
                                promedio_cursada = Calificaciones(
                                cursante=Cursante.objects.get(id=calificacion['cursante']),
                                asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                                valor=promedio,
                                tipo="PROMEDIO CURSADA",  
                                fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                                # Agrega otros campos necesarios según tu modelo
                            )
                                promedio_cursada.save()
                            except ValidationError:
                                print("Ya existe una calificación de promedio cursada")
                                
                            
                            
                    elif periodo.regimen_materia=="TRIMESTRAL":
                        try:
                            nueva_calificacion = Calificaciones(
                                cursante=Cursante.objects.get(id=calificacion['cursante']),
                                asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                                valor=calificacion['promedio'],
                                tipo="PROMEDIO CURSADA",
                                fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                                # Agrega otros campos necesarios según tu modelo
                            )
                            nueva_calificacion.save()  # Se guardará como parte de la transacción
                        except ValidationError:
                                print("Ya existe una calificación de promedio cursada")
                     
                     
                                
                    elif periodo.regimen_materia=="CUATRIMESTRAL":
                        nueva_calificacion = Calificaciones(
                            cursante=Cursante.objects.get(id=calificacion['cursante']),
                            asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                            valor=calificacion['promedio'],
                            tipo=equivalencia_tipo_calificacion[periodo.subPeriodo],  
                            fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                            # Agrega otros campos necesarios según tu modelo
                        )
                        nueva_calificacion.save()  # Se guardará como parte de la transacción
                        
                        if periodo.subPeriodo=="B2_A" or periodo.subPeriodo=="B2_B":
                            try:
                                calificacion_primer_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="BIMESTRAL_1").first()
                                calificacion_segundo_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="BIMESTRAL_2").first()                           
                                promedio=Avg([calificacion_primer_trimestre.valor, calificacion_segundo_trimestre.valor])         
                                promedio_cursada = Calificaciones(
                                cursante=Cursante.objects.get(id=calificacion['cursante']),
                                asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                                valor=promedio,
                                tipo="PROMEDIO CURSADA",  
                                fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                                # Agrega otros campos necesarios según tu modelo
                            )
                                promedio_cursada.save()
                            except ValidationError:
                                print("Ya existe una calificación de promedio cursada")
                        
                        
                        
                        
                    elif periodo.regimen_materia=="SEMESTRAL":
                        nueva_calificacion = Calificaciones(
                            cursante=Cursante.objects.get(id=calificacion['cursante']),
                            asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                            valor=calificacion['promedio'],
                            tipo=equivalencia_tipo_calificacion[periodo.subPeriodo],
                            fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                            # Agrega otros campos necesarios según tu modelo
                        )
                        nueva_calificacion.save()  # Se guardará como parte de la transacción
                        #Si es el último timestre agregamos la calificación de promedio cursada
                        if periodo.subPeriodo=="T2":
                            try:
                                calificacion_primer_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="TRIMESTRAL_1").first()
                                calificacion_segundo_trimestre=Calificaciones.objects.filter(cursante=Cursante.objects.get(id=calificacion['cursante']), asignatura=Asignatura.objects.get(id=calificacion['asignatura']), tipo="TRIMESTRAL_2").first()                           
                                promedio=Avg([calificacion_primer_trimestre.valor, calificacion_segundo_trimestre.valor])         
                                promedio_cursada = Calificaciones(
                                cursante=Cursante.objects.get(id=calificacion['cursante']),
                                asignatura=Asignatura.objects.get(id=calificacion['asignatura']),
                                valor=promedio,
                                tipo="PROMEDIO CURSADA",  
                                fecha_examen=fecha_hoy,  # Ajusta esto según sea necesario
                                # Agrega otros campos necesarios según tu modelo
                            )
                                promedio_cursada.save()
                            except ValidationError:
                               print( "No se pudo calcular el promedio cursada")