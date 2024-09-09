from .views import MateriaCreateView, MateriaListView, MateriaDeleteView, MateriaUpdateView,PlanEstudioCreateView,PlanEstudioListView, PlanEstudioUpdateView, DeletePlanEstudio
from django.urls import path

app_name='cursos'
urlpatterns = [
    path('crear_materia/', MateriaCreateView.as_view(), name='crear_materia'),
    path('ver_materias/', MateriaListView.as_view(), name='ver_materias'),
     path('eliminar_materia/<int:pk>/', MateriaDeleteView.as_view(), name='eliminar_materia'),
     path('modificar_materia/<int:pk>/', MateriaUpdateView.as_view(), name='modificar_materia'),
     path('crear_plan_estudio/', PlanEstudioCreateView.as_view(), name='crear_nuevo_plan_estudio'),
     path('ver_planes_estudio/', PlanEstudioListView.as_view(), name='ver_planes_estudio'),
     path('modificar_plan_estudio/<int:pk>/', PlanEstudioUpdateView.as_view(), name='modificar_plan_estudio'),
     path('eliminar_plan_estudio/<int:pk>/', DeletePlanEstudio.as_view(), name='eliminar_plan_estudio')
    
]