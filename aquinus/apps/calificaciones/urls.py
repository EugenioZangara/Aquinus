from django.urls import path, include
from .views import HomeCalificaciones
app_name='calificaciones'
urlpatterns = [
    path('home/', HomeCalificaciones.as_view(), name="home"),
    
]
