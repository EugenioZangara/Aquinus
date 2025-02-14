from django.db.models import Avg
from django.db.models import Prefetch
from apps.cursos.models import Calificaciones, FechasExamenes, Curso, Cursante

def promediarTrimestre(asignatura, alumno, trimestre, anio_lectivo):
    """
    Calcula el promedio de las calificaciones de un alumno en un trimestre específico.
    
    """
    periodo_trimestre=FechasExamenes.objects.filter(regimenMateria="TRIMESTRAL", subPeriodo="T"+trimestre, anio_lectivo=anio_lectivo, aplica_para=alumno.grado )
    calificaciones_trimestre = Calificaciones.objects.filter(
        asignatura=asignatura,
        cursante__dni=alumno.dni,
        tipo='ORDINARIA', fecha_examen__gte=periodo_trimestre.fechaInicioCalificacion, fecha_examen__lte=periodo_trimestre.fechaTopeCalificacion
    )
    if calificaciones_trimestre.exists():
        promedio_trimestre = calificaciones_trimestre.aggregate(promedio=Avg('valor'))['promedio']
        return promedio_trimestre
    else:
        return None
    
cursos =Curso.objects.filter(activo=True)



# Precalcular los cursantes y asignaturas para todos los cursos
cursos = cursos.prefetch_related(
    Prefetch('cursantes', queryset=Cursante.objects.all(), to_attr='cached_cursantes'),
    Prefetch('asignaturas', to_attr='cached_asignaturas')
)

for curso in cursos:
    cursantes = curso.cached_cursantes  # Cursantes ya precargados
    asignaturas = curso.cached_asignaturas  # Asignaturas ya precargadas
    for cursante in cursantes:
        for asignatura in asignaturas:
            promedio_trimestre_1 = promediarTrimestre(asignatura, cursante, '1', curso.anio_lectivo)
            print(f"Promedio Trimestre 1 para {cursante.nombre} en {asignatura.nombre}: {promedio_trimestre_1}")

    