from django.urls import path, include
from .views import HomeCalificaciones, CalificarView, CalificacionesAsignatura, BoletinView
app_name='calificaciones'
urlpatterns = [
    path('home/', HomeCalificaciones.as_view(), name="home"),
    path('calificar/<int:id>/', CalificarView.as_view(), name="calificar"),
    path('calificaciones_asignatura/<int:id>/', CalificacionesAsignatura.as_view(), name="calificaciones_asignatura"),
    path('boletin/<int:dni>/', BoletinView.as_view(), name="boletin"),
    
]
