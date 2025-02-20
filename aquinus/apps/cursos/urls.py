from .views import MateriaCreateView, MateriaListView, MateriaDeleteView, MateriaUpdateView,PlanEstudioCreateView,PlanEstudioListView, PlanEstudioUpdateView, DeletePlanEstudio, PlanEstudioDetailView, CursoCreateView, CursoListView, CursoDeleteView, CursoDetailView, AsignarProfesores,  ProfesorTemplateView, AlumnosCursoUpdateView, VerFechasMaterias, DefinirFechas, update_fechas, fijarInicioAnioLectivo, AsignarPeriodoCursada
from .views_htmx import get_orientaciones, seleccionar_registro, quitar_registro, agregar_registro, agregarFormularioPeriodoCursada
from django.urls import path
from apps.utils.generador_boletines import generar_boletin_pdf

app_name='cursos'
urlpatterns = [
    path('crear_materia/', MateriaCreateView.as_view(), name='crear_materia'),
    path('ver_materias/', MateriaListView.as_view(), name='ver_materias'),
     path('eliminar_materia/<int:pk>/', MateriaDeleteView.as_view(), name='eliminar_materia'),
     path('modificar_materia/<int:pk>/', MateriaUpdateView.as_view(), name='modificar_materia'),
     path('crear_plan_estudio/', PlanEstudioCreateView.as_view(), name='crear_nuevo_plan_estudio'),
     path('ver_planes_estudio/', PlanEstudioListView.as_view(), name='ver_planes_estudio'),
     path('modificar_plan_estudio/<int:pk>/', PlanEstudioUpdateView.as_view(), name='modificar_plan_estudio'),
     path('eliminar_plan_estudio/<int:pk>/', DeletePlanEstudio.as_view(), name='eliminar_plan_estudio'),
     path('detalles_plan_estudio/<int:pk>/', PlanEstudioDetailView.as_view(), name='detalles_plan_estudio'),
     path('crear_curso/', CursoCreateView.as_view(), name='crear_curso'),
     path('ver_cursos/', CursoListView.as_view(), name='ver_cursos'),
     path('eliminar_curso/<int:pk>/', CursoDeleteView.as_view(), name='eliminar_curso'), 
     path('detalles_curso/<int:pk>/', CursoDetailView.as_view(), name='detalles_curso'),
     path('get_orientaciones/', get_orientaciones, name='get_orientaciones') ,#htmx para generar opciones dinámicamente para las orientaciones
    path('seleccionar_registro/<int:id>/',seleccionar_registro, name='seleccionar_registro'),
        path('agregar_registro/<int:id>/',agregar_registro, name='agregar_registro'),

     path('quitar_registro/<int:id>/',quitar_registro, name='quitar_registro'),
     path('asignar_profesores/<int:pk>/', AsignarProfesores.as_view(), name='asignar_profesores'),
  
     path('actualizar_profesores_materias/<int:materia_id>/', ProfesorTemplateView.as_view(), name='actualizar_profesores_materias'),
     path('modificar_alumnos_curso/<int:pk>/', AlumnosCursoUpdateView.as_view(), name='modificar_alumnos_curso'),
     path ('VerFechasMaterias/', VerFechasMaterias.as_view(),name='ver_fechas_materias'),
    path('definir_fechas/', DefinirFechas.as_view(), name="definir_fechas"),
    path('update_fechas/<int:pk>/', update_fechas.as_view(), name='update_fechas'),
    path('fijarInicioAnioLectivo/',fijarInicioAnioLectivo, name="fijar_inicio_anio_lectivo"),
    #path('asignar_periodos/', AsignarPeriodoCursada.as_view(), name="asignar_periodos"),
    path('asignar_periodos/<int:pk>/', AsignarPeriodoCursada.as_view(), name="asignar_periodos"),
    path('agregarFormularioPeriodoCursada/<int:id>/', agregarFormularioPeriodoCursada, name='agregar_formulario_periodo_cursada'),
    path('generar_boletin_pdf/<int:pk>/', generar_boletin_pdf, name="generar_boletin_pdf"),#url para generar boletines en pdf
]

