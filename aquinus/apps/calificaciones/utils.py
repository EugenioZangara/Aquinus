from datetime import datetime
from django.db.models import Q
from apps.cursos.models import FechasExamenes


def periodoMateria(asignatura):
    fechaActual = datetime.now()
    
    tipo_asignatura = asignatura.materia.tipo
    
    try: 
        fechasMaterias = FechasExamenes.objects.filter(
        regimen_materia=asignatura.materia.tipo,
        anio_lectivo=fechaActual.year,
    ).get(regimen_materia=tipo_asignatura,aplica_para=asignatura.materia.anio , fechaInicioCalificacion__lt=fechaActual, fechaTopeCalificacion__gt=fechaActual)
        
        
    except FechasExamenes.DoesNotExist:
        fechasMaterias = FechasExamenes.objects.filter(
            regimen_materia=asignatura.materia.tipo,
            anio_lectivo=fechaActual.year,
        ).get(regimen_materia=tipo_asignatura,aplica_para="TODOS", fechaInicioCalificacion__lt=fechaActual, fechaTopeCalificacion__gt=fechaActual)
    except FechasExamenes.MultipleObjectsReturned:
      
        fechasMaterias = FechasExamenes.objects.filter(
            regimen_materia=asignatura.materia.tipo)
        
    

    except FechasExamenes.DoesNotExist:
        print("NO ENCONTRÓ NINGUNO")
        
    
    return convertirPeriodos(fechasMaterias.subPeriodo)

def convertirPeriodos(periodo):
    if periodo == 'T1':
        return 'Primer Trimestre'
    elif periodo == 'T2':
        return 'Segundo Trimestre'
    elif periodo == 'T3':
        return 'Tercer Trimestre' 
    elif periodo == 'FS_A':
        return 'Examen Final Primer Semestre'
    elif periodo == 'FS_B':
        return 'Examen Final Segundo Semestre'
    elif periodo == 'B1_A':
        return 'Primer Bimestre - 1er. Cuatrimestre'
    elif periodo == 'B2_A':
        return 'Cierre Primer Cuatrimestre'
    elif periodo == 'FC_A':
        return 'Final Primer Cuatrimestre'
    elif periodo == 'B1_B':
        return 'Primer Bimestre - 2do. Cuatrimestre'
    elif periodo == 'B2_B':
        return 'Cierre Segundo Cuatrimestre'
    elif periodo== 'FC_B':
        return 'Final Segundo Cuatrimestre'     
    elif periodo == 'FT_1':
        return 'Final Primer Trimestre'
    elif periodo == 'FT_2':
        return 'Final Segundo Trimestre'
    elif periodo == 'FT_3':
        return 'Final Tercer Trimestre'
    elif periodo=="FA":
        return "Final Anual"
    else:
        print("periodo", periodo)
        return "Periodo no encontrado"