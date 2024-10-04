from django.shortcuts import render
from django.views.generic import TemplateView
from apps.cursos.models import Asignatura, Cursante, Calificaciones
from django.db.models import Count
from django.forms import formset_factory, modelformset_factory
from django.contrib import messages

from apps.alumnos.models import persona
from .forms import CalificacionesForm
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
    
    
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

class CalificarView(TemplateView):
    template_name = "calificaciones/calificar.html"
    success_url = 'calificaciones:home'
    
    def get_asignatura(self):
        return get_object_or_404(Asignatura, id=self.kwargs['id'])
    
    def get_alumnos(self, asignatura):
        dni_cursantes = list(Cursante.objects.filter(curso=asignatura.curso).values_list('dni', flat=True))
        return persona.objects.filter(dni__in=dni_cursantes).using('id8')
    
    def get_formset(self, data=None):
        asignatura = self.get_asignatura()
        alumnos = self.get_alumnos(asignatura)
        CalificacionFormSet = modelformset_factory(Calificaciones, form=CalificacionesForm, extra=len(alumnos))
        queryset = Calificaciones.objects.none()
        return CalificacionFormSet(data, queryset=queryset), alumnos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura = self.get_asignatura()
        formset, alumnos = self.get_formset()
        forms_and_alumnos = zip(formset, alumnos)
        context["asignatura"] = asignatura
        context["forms_and_alumnos"] = forms_and_alumnos
        context["formset"] = formset  # Agregamos el formset al contexto
        return context
    
    def post(self, request, *args, **kwargs):
        formset, alumnos = self.get_formset(request.POST)
        asignatura = self.get_asignatura()
        
        print("Datos POST:", request.POST)
        
        if formset.is_valid():
            instances = formset.save(commit=False)

            for instance, alumno in zip(instances, alumnos):
                if instance.valor is not None:
                    cursante=Cursante.objects.get(dni=alumno.dni)
                    instance.cursante = cursante
                    instance.asignatura = asignatura
                    instance.valor = instance.valor
                    instance.tipo="ORDINARIA"
                    instance.calificador=self.request.user.perfil
                    instance.save()
            messages.success(request, f'Calificación para cargadas correctamente.')
            return redirect(self.success_url)
        else:
            print("Errores en el formset:", formset.errors)
            for form in formset:
                print("Error en el form individual:", form.errors)
        
        # Si el formset no es válido, mostrar el formulario nuevamente
        return self.render_to_response(self.get_context_data(formset=formset))

