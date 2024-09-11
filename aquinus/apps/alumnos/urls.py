from django.urls import path
from .views import get_alumnos_por_especialidad
app_name = 'alumnos'

urlpatterns = [
    path('alumnosPorEspecialidad/', get_alumnos_por_especialidad, name='alumnos_por_especialidad'),
]
