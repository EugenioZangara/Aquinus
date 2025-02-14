from django.core.exceptions import ValidationError
from datetime import datetime
import re
from django.core.management.base import BaseCommand
from django.db.models import Avg, Prefetch
from apps.cursos.models import Calificaciones, FechasExamenes, Curso, Cursante

class Command(BaseCommand):
    help = 'Calcula promedios de trimestre para los cursantes y los imprime en la terminal'

    def handle(self, *args, **kwargs):
        
        def promediarTrimestre(asignatura, alumno, trimestre, aplica_para, anio_lectivo):
            trim = "T" + trimestre
            periodo_trimestre = FechasExamenes.objects.filter(
                regimen_materia="TRIMESTRAL", subPeriodo=trim, anio_lectivo=anio_lectivo, aplica_para=aplica_para
            ).first()
            
            if not periodo_trimestre:
                return None
            calificaciones_trimestre = Calificaciones.objects.filter(
                asignatura=asignatura,
                cursante__dni=alumno.dni,
                tipo='ORDINARIA',
                fecha_examen__gte=periodo_trimestre.fechaInicioCalificacion,
                fecha_examen__lte=periodo_trimestre.fechaTopeCalificacion
            )
            if calificaciones_trimestre.exists():
                promedio_trimestre = calificaciones_trimestre.aggregate(promedio=Avg('valor'))['promedio']                
                return promedio_trimestre
            else:
                return None

        def promediarBimestres(asignatura, alumno, bimestre,ciclo, aplica_para, anio_lectivo):
            bim="B"+bimestre+"_"+ciclo
            
            periodo_bimestre = FechasExamenes.objects.filter(
                regimen_materia="CUATRIMESTRAL", subPeriodo=bim, anio_lectivo=anio_lectivo, aplica_para=aplica_para
            ).first()
            if not periodo_bimestre:
                return None
            calificaciones_bimestre = Calificaciones.objects.filter(
                asignatura=asignatura,
                cursante__dni=alumno.dni,
                tipo='ORDINARIA',
                fecha_examen__gte=periodo_bimestre.fechaInicioCalificacion,
                fecha_examen__lte=periodo_bimestre.fechaTopeCalificacion
            )
            if calificaciones_bimestre.exists():
                promedio_bimestre = calificaciones_bimestre.aggregate(promedio=Avg('valor'))['promedio']
                return promedio_bimestre
            else:
                return None

        def promediarCursadaAnual(asignatura, alumno, aplica_para, anio_lectivo):
            notasParciales=['TRIMESTRAL_1', "TRIMESTRAL_2", "TRIMESTRAL_3"]
            calificacionesAnuales=Calificaciones.objects.filter(asignatura=asignatura, 
                                                                cursante__dni=alumno.dni, 
                                                                tipo__in=notasParciales,
                                                                fecha__year=anio_lectivo 
                                                                )
            if calificacionesAnuales.exists():
                promedio_anual = calificacionesAnuales.aggregate(promedio=Avg('valor'))['promedio']
                return promedio_anual
            else:
                return None
        def promediarCursadaSemestral(asignatura, alumno, aplica_para, anio_lectivo):
            notasParciales=['TRIMESTRAL_1', "TRIMESTRAL_2", "TRIMESTRAL_3"]
            calificacionesTrimestralesAnuales=Calificaciones.objects.filter(asignatura=asignatura,
                                                                cursante__dni=alumno.dni,
                                                                tipo__in=notasParciales,
                                                                fecha__year=anio_lectivo
                                                                )
            if calificacionesTrimestralesAnuales.exists():
                promedio_semestral = calificacionesTrimestralesAnuales.aggregate(promedio=Avg('valor'))['promedio']
                return promedio_semestral
            else:
                return None
        
        def promediarCursadaCuatrimestral(asignatura, alumno, aplica_para, anio_lectivo):
            notasParciales=['BIMESTRAL_1', "BIMESTRAL_2", "BIMESTRAL_3","BIMESTRAL_4"]
            calificacionesCuatrimestrales=Calificaciones.objects.filter(asignatura=asignatura,
                                                                cursante__dni=alumno.dni,
                                                                tipo__in=notasParciales,
                                                                fecha__year=anio_lectivo
                                                                )
            if calificacionesCuatrimestrales.exists():
                promedio_cuatrimestral = calificacionesCuatrimestrales.aggregate(promedio=Avg('valor'))['promedio']
                return promedio_cuatrimestral
            else:
                return None
             
        cursos = Curso.objects.filter(activo=True).prefetch_related(
            Prefetch('alumno_curso', queryset=Cursante.objects.all(), to_attr='cached_cursantes'),
            Prefetch('asignaturas', to_attr='cached_asignaturas')
        )

        # Obtener el tiempo actual una sola vez
        fecha_examen_actual = datetime.now()

        # Lista para almacenar los nuevos registros a crear
        nuevos_promedios = []

        for curso in cursos:
            # Extraer el año solo una vez por curso
            anio = re.search(r'(\d{4})', curso.nombre)
            anio_curso = int(anio.group(1)) if anio else None
            cursantes = curso.cached_cursantes
            asignaturas = curso.cached_asignaturas
            promedioCursadaAnual=None
            promedioCursadaSemestral=None
            promedioCursadaCuatrimestral=None
            for cursante in cursantes:
                for asignatura in asignaturas:
                    promedio_trimestre_1 = promediarTrimestre(asignatura, cursante, '1', curso.anio, anio_curso)
                    promedio_trimestre_2 = promediarTrimestre(asignatura, cursante, '2', curso.anio, anio_curso)
                    promedio_trimestre_3 = promediarTrimestre(asignatura, cursante, '3', curso.anio, anio_curso)
                    promedio_bimestre_1A=promediarBimestres(asignatura, cursante, '1', 'A', curso.anio, anio_curso)
                    promedio_bimestre_1B=promediarBimestres(asignatura, cursante, '1', 'B', curso.anio, anio_curso)
                    promedio_bimestre_2A=promediarBimestres(asignatura, cursante, '2', 'A', curso.anio, anio_curso)
                    promedio_bimestre_2B=promediarBimestres(asignatura, cursante, '2', 'B', curso.anio, anio_curso)
                    if asignatura.materia.tipo=="ANUAL":
                        promedioCursadaAnual=promediarCursadaAnual(asignatura, cursante, curso.anio, anio_curso)
                    if asignatura.materia.tipo=="SEMESTRAL":
                        promedioCursadaSemestral=promediarCursadaSemestral(asignatura, cursante, curso.anio, anio_curso)
                    if asignatura.materia.tipo=="CUATRIMESTRAL":
                        promedioCursadaCuatrimestral=promediarCursadaCuatrimestral(asignatura, cursante, curso.anio, anio_curso)
                    if promedio_trimestre_1 is not None:
                        calificacion_1 = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_trimestre_1,
                            tipo="TRIMESTRAL_1",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_1.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_1)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")
                    if promedio_trimestre_2 is not None:
                        calificacion_2 = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_trimestre_2,
                            tipo="TRIMESTRAL_2",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_2.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_2)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")
                    if promedio_trimestre_3 is not None:
                        calificacion_3 = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_trimestre_3,
                            tipo="TRIMESTRAL_3",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_3.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_3)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")                            
                    if promedio_bimestre_1A is not None:
                        calificacion_1A = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_bimestre_1A,
                            tipo="BIMESTRAL_1",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_1A.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_1A)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")                           
                    if promedio_bimestre_1B is not None:
                        calificacion_1B = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_bimestre_1B,
                            tipo="BIMESTRAL_1",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_1B.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_1B)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")  
                    if promedio_bimestre_2A is not None:
                        calificacion_2A = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_bimestre_2A,
                            tipo="BIMESTRAL_2",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_2A.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_2A)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")    
                    if promedio_bimestre_2B is not None:
                        calificacion_2B = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedio_bimestre_2B,
                            tipo="BIMESTRAL_2",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_2B.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_2B)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")
                    if promedioCursadaAnual is not None:
                        calificacion_cursada_anual = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedioCursadaAnual,
                            tipo="PROMEDIO CURSADA",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_cursada_anual.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_cursada_anual)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")
                    if promedioCursadaSemestral is not None:
                        calificacion_cursada_semestral = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedioCursadaSemestral,
                            tipo="PROMEDIO CURSADA",
                            fecha_examen=fecha_examen_actual,
                        ) 
                        try:
                            calificacion_cursada_semestral.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_cursada_semestral)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")
                    if promedioCursadaCuatrimestral is not None:
                        calificacion_cursada_cuatrimestral = Calificaciones(
                            asignatura=asignatura,
                            cursante=cursante,
                            valor=promedioCursadaCuatrimestral,
                            tipo="PROMEDIO CURSADA",
                            fecha_examen=fecha_examen_actual,
                        )
                        try:
                            calificacion_cursada_cuatrimestral.clean()  # Llamar la validación personalizada
                            nuevos_promedios.append(calificacion_cursada_cuatrimestral)
                        except ValidationError as e:
                            self.stdout.write(f"Error en la validación para {cursante} - {asignatura}: {e}")
        # Crear los registros en lote (bulk_create)
        if nuevos_promedios:
            Calificaciones.objects.bulk_create(nuevos_promedios)
            self.stdout.write(f"{len(nuevos_promedios)} nuevos registros de calificaciones creados.")


