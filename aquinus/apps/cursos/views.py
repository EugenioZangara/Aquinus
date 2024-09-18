from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView, TemplateView
import json
from django.db import IntegrityError, transaction
from apps.alumnos.models import persona
from apps.usuarios.models import Perfil
from .models import Materia, PlanEstudio ,Curso, Cursante, Profesor
from .forms import MateriaForm, MateriaEditForm,PlanEstudioForm, CursoCreateForm,  AsignarProfesoresForm
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
        try:
            # Crea el curso pero no lo guarda aún
            self.curso = form.save(commit=False)
            self.curso.activo = True
            self.curso.puede_calificar = True
            # No guardar aún
            return super().form_valid(form)
        except IntegrityError as e:
             
                # Manejar errores de integridad (como el nombre del curso duplicado)
                messages.error(self.request, 'El nombre del curso ya existe. Por favor, elige otro.')
                return self.form_invalid(self.get_form()) 
            
        

    def form_invalid(self, form):
            # Aquí puedes manejar cómo se muestran los errores en el formulario
            return self.render_to_response(self.get_context_data(form=form))
        
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
                curso.save(request=request)  #PASAMOS EL REQUEST PARA ALMACENAR EL USUARIO QUE REALIZÓ EL CAMBIO
                # Mensaje de éxito
                messages.success(request, 'El curso se ha creado y se han asociado los alumnos correctamente.')
            except IntegrityError as e:
                # Manejar errores de integridad (como el nombre del curso duplicado)
                messages.error(request, 'El nombre del curso ya existe. Por favor, elige otro.')
                return self.form_invalid(self.get_form())    
            except Exception as e:
                # Si ocurre un error, la transacción se revertirá
                messages.error(request, f'Hubo un error al asociar los alumnos: {str(e)}')
                return self.form_invalid(self.get_form())

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
        dni_cursantes=Cursante.objects.filter(curso=curso).values_list('dni', flat=True)
        cursantes=persona.objects.using('id8').filter(dni__in=list(dni_cursantes))
        # Agrega las materias al contexto
        context['materias'] = materias
        context['cursantes']=cursantes
        
        return context
    
class AsignarProfesores(ListView):
    model=Materia
    template_name='cursos/materias/asignar_profesores.html'
    context_object_name='materias'
    

    def get_queryset(self):
        curso_id=self.kwargs.get('pk')
        curso = Curso.objects.get(id=curso_id)
        materias=Materia.objects.filter(materias_plan_de_estudio=curso.plan_de_estudio).prefetch_related('profesor_materia')
        return materias

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(pk=self.kwargs['pk'])
        materias = curso.plan_de_estudio.materias.all()

        # Crear una lista de tuplas (materia, formulario)
        
        context['curso']=curso
        context['materias'] = materias
        return context
    
class ProfesorTemplateView(TemplateView):
    model = Profesor
    template_name = "cursos/materias/actualizar_profesores.html"
    
    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        materia_id = kwargs.get('materia_id')
        curso_id = kwargs.get('curso_id')
        materia = get_object_or_404(Materia, id=materia_id)
        curso = get_object_or_404(Curso, id=curso_id)
    
        
        # Obtener los profesores existentes para este curso y materia
        profesores_existentes = Profesor.objects.filter(curso=curso, materias=materia)
        
        # Obtener los IDs de los usuarios de los profesores existentes
        usuarios_existentes = [prof.usuario.usuario.id for prof in profesores_existentes]
        
        form = AsignarProfesoresForm(initial={'usuario': usuarios_existentes})
        context["form"]=form
        context["materia"] =materia
        context["curso"]=curso 
        return context
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        curso = context['curso']
        materia = context['materia']
        form = AsignarProfesoresForm(request.POST)
        
        if form.is_valid():
            usuarios_seleccionados = set(form.cleaned_data['usuario'])
            
            # Obtener todos los profesores actualmente asignados a este curso y materia
            profesores_actuales = Profesor.objects.filter(curso=curso, materias=materia)
            usuarios_actuales = set(profesor.usuario.usuario for profesor in profesores_actuales)
            
            # Identificar usuarios deseleccionados
            usuarios_deseleccionados = usuarios_actuales - usuarios_seleccionados
            
            # Eliminar las asignaciones existentes para usuarios deseleccionados
            for usuario in usuarios_deseleccionados:
                profesor = profesores_actuales.get(usuario__usuario=usuario)
                profesor.curso.remove(curso)
                profesor.materias.remove(materia)
                messages.warning(request, f'Se ha eliminado la asignación del profesor {profesor.usuario} para este curso y materia.')
            
            # Crear o actualizar las nuevas asignaciones
            for usuario in usuarios_seleccionados:
                perfil = usuario.perfil
                profesor, created = Profesor.objects.get_or_create(usuario=perfil)
                profesor.curso.add(curso)
                profesor.materias.add(materia)
                
                if created:
                    messages.success(request, f'El profesor {perfil} ha sido creado y asignado correctamente.')
                elif usuario not in usuarios_actuales:
                    messages.success(request, f'El profesor {perfil} ha sido asignado correctamente.')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
            context['form'] = form
            return self.render_to_response(context)


        # Redirigir pasando los ids de curso y materia
        return redirect(reverse_lazy('cursos:asignar_profesores', kwargs={'pk': curso.id}))





def obtener_formulario_asignar_profesores(request):
    materia_id = request.GET.get('materia_id')
    materia = get_object_or_404(Materia, id=materia_id)

    form = AsignarProfesoresForm(materia=materia)
    return render(request, 'cursos/materias/partials/formulario_asignar_profesores.html', {'form': form, 'materia': materia})

def actualizar_profesores_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    
    if request.method == 'POST':
        form = AsignarProfesoresForm(request.POST)
        if form.is_valid():
            profesores = form.cleaned_data['profesores']
            materia.profesor_materia.set(profesores)  # Actualizar los profesores asociados a la materia
            materia.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})