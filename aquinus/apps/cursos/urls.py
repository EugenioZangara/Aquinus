from .views import MateriaCreateView, MateriaListView, MateriaDeleteView
from django.urls import path

app_name='cursos'
urlpatterns = [
    path('crear_materia/', MateriaCreateView.as_view(), name='crear_materia'),
    path('ver_materias/', MateriaListView.as_view(), name='ver_materias'),
     path('eliminar_materia/<int:pk>/', MateriaDeleteView.as_view(), name='eliminar_materia'),
    
]