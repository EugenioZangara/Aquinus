from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import  get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
import json
from django.db import transaction
from apps.alumnos.models import persona
from .models import Materia, PlanEstudio ,Curso, Cursante
from .forms import MateriaForm, MateriaEditForm,PlanEstudioForm, CursoCreateForm
# Create your views here.

class MateriaCreateView(CreateView):
    form_class = MateriaForm
    template_name = "cursos/materias/crear_materia.html"
    success_url=reverse_lazy('home')
    
    def form_valid(self, form):
       
        if form.is_valid() :
            messages.success(self.request, 'Materia creada con éxito.')
            return super().form_valid(form)  # Redirige a la URL de éxito.
        else:
            # Mensaje de error en caso de datos inválidos.
            messages.error(self.request, 'Hubo un error al crear la materia. Verifica los datos e inténtalo de nuevo.')
            return self.form_invalid(form)  # Redirige a la misma página mostrando los errores.

class MateriaListView(ListView):
    model = Materia
    template_name = "cursos/materias/ver_materias.html"
    context_object_name = 'materias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="materias"   
        return context
    
class MateriaDeleteView(SuccessMessageMixin,DeleteView):
    model = Materia
    success_url = reverse_lazy('cursos:ver_materias')  
    success_message = "La materia %(nombre)s ha sido eliminada exitosamente."

    # Este método se asegura de pasar el objeto al success_message
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.nombre
        )

class MateriaUpdateView(SuccessMessageMixin, UpdateView):
    model = Materia
    template_name = "cursos/materias/modificar_materia.html"
    form_class = MateriaForm
    success_url = reverse_lazy('cursos:ver_materias') 
    success_message = "La materia %(nombre)s ha sido modificada exitosamente."

    
    # Este método se asegura de pasar el objeto al success_message
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.nombre
        )
        
class PlanEstudioCreateView(CreateView):
    model = PlanEstudio
    template_name = "cursos/planes_estudio/crear_plan_estudios.html"
    success_url=reverse_lazy('home')
    form_class=PlanEstudioForm
    #success_message = "Se ha creado el plan de estudio para la especialidad %(especialidad) exitosamente."
    
    
    
    def form_valid(self, form):
        # Guardar el objeto primero
        response = super().form_valid(form)
        # Acceder a la especialidad del objeto creado
        especialidad = self.object.especialidad
        # Mostrar el mensaje de éxito
        messages.success(self.request, f"Se ha creado el plan de estudio para la especialidad {especialidad} exitosamente.")
        print(form.cleaned_data)
        return response
    
    def form_invalid(self, form):
       
        # Imprimir los errores del formulario en la consola
        print("Formulario inválido. Errores:", form.errors)
        # También puedes registrar los errores usando logging
        # Mostrar mensaje de error en la página
        messages.error(self.request, "Ocurrió un error al crear el plan de estudio. Por favor, revisa los datos ingresados.")
        return super().form_invalid(form)
    
class PlanEstudioListView(ListView):
    model = PlanEstudio
    template_name = "cursos/planes_estudio/ver_planes_estudio.html"
    context_object_name = 'planes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planes=PlanEstudio.objects.filter(vigente=True)
        context['active_tab']="planes_estudio" 
        context['planes']=planes  
        return context
    
    def get_queryset(self):
        # Hacemos un select_related para traer el perfil asociado al usuario
        # Filtramos solo los usuarios que están activos (is_active=True)
        return PlanEstudio.objects.filter(vigente=True)
    
class PlanEstudioUpdateView(SuccessMessageMixin,UpdateView):
    model = PlanEstudio
    template_name = "cursos/planes_estudio/modificar_plan_estudio.html"
    form_class = PlanEstudioForm
    success_url = reverse_lazy('cursos:ver_planes_estudio') 
    success_message = "El Plan de Estudio perteneciente a la especialidad %(especialidad) ha sido modificado exitosamente."

    
    # Este método se asegura de pasar el objeto al success_message
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.especialidad
        )
    
    

class DeletePlanEstudio(View):
    success_url = reverse_lazy('cursos:ver_planes_estudio')  # Redirigir al listado de planes de estudio

    def post(self, request, pk, *args, **kwargs):
        # Obtiene el plan de estudio por el pk (clave primaria) o devuelve 404 si no existe
        plan_estudio = get_object_or_404(PlanEstudio, pk=pk)
        
        # Cambiar el estado vigente a False para hacer la eliminación lógica
        plan_estudio.vigente = False
        plan_estudio.save()
        messages.success(self.request, 'Plan de estudio eliminado con éxito.')
        # Redirigir a la URL definida en success_url
        return redirect(self.success_url)
    
class PlanEstudioDetailView(DetailView):
    model = PlanEstudio
    template_name = "cursos/planes_estudio/detalles.html"
    context_object_name='plan_de_estudio'


class CursoCreateView(CreateView):
    model = Curso
    template_name = "cursos/cursos/crear_curso.html"
    success_url = reverse_lazy('home')
    form_class = CursoCreateForm

    def form_valid(self, form):
        # Crea el curso pero no lo guarda aún
        self.curso = form.save(commit=False)
        self.curso.activo = True
        self.curso.puede_calificar = True
        # No guardar aún
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # Procesar el formulario
        response = super().post(request, *args, **kwargs)

        # Obtener los alumnos seleccionados del request
        alumnos = request.POST.get('alumnos_seleccionados')
        try:
            alumnos_seleccionados = json.loads(alumnos)
        except json.JSONDecodeError:
            alumnos_seleccionados = []

        curso = self.curso  # Curso no guardado aún
        
        # Empezar una transacción
        with transaction.atomic():
            try:
                for alumno_dni in alumnos_seleccionados:
                    Cursante.objects.create(dni=alumno_dni, curso=curso)
                
                # Guardar el curso después de asociar todos los alumnos
                curso.save()
                # Mensaje de éxito
                messages.success(request, 'El curso se ha creado y se han asociado los alumnos correctamente.')
                
            except Exception as e:
                # Si ocurre un error, la transacción se revertirá
                messages.error(request, f'Hubo un error al asociar los alumnos: {str(e)}')
                response = redirect(self.success_url)
                return response

        # Redirigir a la URL de éxito después de agregar el mensaje
        return redirect(self.success_url)
    
class CursoListView(ListView):
    model = Curso
    template_name = "cursos/cursos/ver_cursos.html"
    context_object_name="cursos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="cursos"   
        return context
    
class CursoDeleteView(SuccessMessageMixin, DeleteView):
    model = Curso
    success_url = reverse_lazy('cursos:ver_cursos')  # Redirigir al listado de planes de estudio
    success_message = "El curso %(nombre) ha sido eliminado exitosamente."


    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.nombre
        )
        
class CursoDetailView(DetailView):
    model = Curso
    template_name = "cursos/cursos/detalles.html"
    context_object_name='cursos'

    def get_context_data(self, **kwargs):
        # Obtén el contexto original de la vista
        context = super().get_context_data(**kwargs)
        
        # Accede al curso actual
        curso = self.object
        
        # Accede al plan de estudio asociado al curso
        plan_de_estudio = curso.plan_de_estudio
        
        # Obtén las materias asociadas al plan de estudio
        materias = plan_de_estudio.materias.all()
        
        # Agrega las materias al contexto
        context['materias'] = materias
        
        return context