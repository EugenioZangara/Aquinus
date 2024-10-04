from django.urls import path, include
from .views import HomeCalificaciones, CalificarView
app_name='calificaciones'
urlpatterns = [
    path('home/', HomeCalificaciones.as_view(), name="home"),
    path('calificar/<int:id>/', CalificarView.as_view(), name="calificar"),
    
]
