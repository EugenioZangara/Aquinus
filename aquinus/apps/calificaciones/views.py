from django.shortcuts import render
from django.views.generic import TemplateView
from apps.cursos.models import Asignatura, Cursante
from django.db.models import Count
# Create your views here.

class HomeCalificaciones(TemplateView):
    template_name="calificaciones/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil_usuario=self.request.user.perfil
        asignaturas=Asignatura.objects.filter(profesor=perfil_usuario).all().order_by('materia')
        asignaturas_con_alumnos={}
        for asignatura in asignaturas:
            cantidad_alumnos_por_curso = Cursante.objects.filter(curso=asignatura.curso).aggregate(total=Count('id'))['total']
            asignaturas_con_alumnos[asignatura]=cantidad_alumnos_por_curso
        context["asignaturas_con_alumnos"] = asignaturas_con_alumnos
        return context
    