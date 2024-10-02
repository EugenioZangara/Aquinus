"""
URL configuration for aquinus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
        path("select2/", include("django_select2.urls")),

    path('usuarios/', include('apps.usuarios.urls',namespace='usuarios')),  # Incluye las URLs de la aplicación 'usuarios'
    path('', include('apps.main.urls')),  # Incluye las URLs de la aplicación 'main'
    path('cursos/', include('apps.cursos.urls',namespace='cursos')),  # Incluye las URLs de la aplicación 'cursos'
path('alumnos/', include('apps.alumnos.urls',namespace='alumnos')),  # Incluye las URLs de la aplicación 'alumnos'
]





# Función personalizada para manejar el error 403
def error_403_view(request, exception=None):
    return render(request, 'errores/403-forbidden/403.html', status=403)

# Asigna la vista personalizada al handler 403
handler403 = error_403_view
