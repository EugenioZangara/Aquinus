import datetime
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.db.models import Prefetch
from datetime import timezone
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView, TemplateView, FormView
import json
from django.db import IntegrityError, transaction
from apps.alumnos.models import persona
from apps.usuarios.models import Perfil
from .models import Materia, PlanEstudio ,Curso, Cursante, Profesor, FechasExamenes
from .forms import MateriaForm, MateriaEditForm,PlanEstudioForm, CursoCreateForm,  AsignarProfesoresForm, FechasCreateForm
from apps.usuarios.mixins.roles_mixins import MultipleRolesRequiredMixin

# Create your views here.

class MateriaCreateView(MultipleRolesRequiredMixin,CreateView):
    form_class = MateriaForm
    template_name = "cursos/materias/crear_materia.html"
    success_url=reverse_lazy('home')
    required_roles = ['STAFF', 'ADMINISTRADOR']

    
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
    
class MateriaDeleteView(MultipleRolesRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Materia
    success_url = reverse_lazy('cursos:ver_materias')  
    success_message = "La materia %(nombre)s ha sido eliminada exitosamente."
    required_roles = ['STAFF', 'ADMINISTRADOR']

    # Este método se asegura de pasar el objeto al success_message
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.nombre
        )
        

class MateriaUpdateView(MultipleRolesRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Materia
    template_name = "cursos/materias/modificar_materia.html"
    form_class = MateriaForm
    success_url = reverse_lazy('cursos:ver_materias') 
    success_message = "La materia %(nombre)s ha sido modificada exitosamente."
    required_roles = ['STAFF', 'ADMINISTRADOR']

    
    # Este método se asegura de pasar el objeto al success_message
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.nombre
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="materias"   
        return context
       
class PlanEstudioCreateView(MultipleRolesRequiredMixin,CreateView):
    model = PlanEstudio
    template_name = "cursos/planes_estudio/crear_plan_estudios.html"
    success_url=reverse_lazy('home')
    form_class=PlanEstudioForm
    required_roles = ['STAFF', 'ADMINISTRADOR']

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="planes_estudio"   
        return context
    
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
    
class PlanEstudioUpdateView(MultipleRolesRequiredMixin,SuccessMessageMixin,UpdateView):
    model = PlanEstudio
    template_name = "cursos/planes_estudio/modificar_plan_estudio.html"
    form_class = PlanEstudioForm
    success_url = reverse_lazy('cursos:ver_planes_estudio') 
    success_message = "El Plan de Estudio perteneciente a la especialidad %(especialidad) ha sido modificado exitosamente."
    required_roles = ['STAFF', 'ADMINISTRADOR']

    
    # Este método se asegura de pasar el objeto al success_message
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            nombre=self.object.especialidad
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="planes_estudio"   
        return context
    

class DeletePlanEstudio(MultipleRolesRequiredMixin,View):
    success_url = reverse_lazy('cursos:ver_planes_estudio')  # Redirigir al listado de planes de estudio
    required_roles = ['STAFF', 'ADMINISTRADOR']

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="planes_estudio"   
        return context
    
class CursoCreateView(MultipleRolesRequiredMixin,CreateView):
    model = Curso
    template_name = "cursos/cursos/crear_curso.html"
    success_url = reverse_lazy('home')
    form_class = CursoCreateForm
    required_roles = ['STAFF', 'ADMINISTRADOR']

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="cursos"   
        return context
    
class CursoListView(ListView):
    model = Curso
    template_name = "cursos/cursos/ver_cursos.html"
    context_object_name="cursos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cursos_activos = Curso.objects.filter(activo=True)
        cursos_con_materias_y_profesores = {}
        for curso in cursos_activos:
            plan_estudio = curso.plan_de_estudio  # Suponiendo que existe un campo plan_de_estudio en Curso
            #materias = plan_estudio.materias.all()
            materias = plan_estudio.materias.filter(anio=curso.anio)
            todas_materias_con_profesores = True  # Se asume que todas tienen profesor inicialmente
            cantidad_alumnos_por_curso = Cursante.objects.filter(curso=curso).aggregate(total=Count('id'))['total']
            # Para cada materia, verificamos si tiene profesores asociados
            materias_con_profesores = []
            for materia in materias:
                tiene_profesor = Profesor.objects.filter(materias=materia).exists()
                materias_con_profesores.append({
                    'materia': materia,
                    'tiene_profesor': tiene_profesor
                })
                 # Si alguna materia no tiene profesor, cambia el flag a False
                if not tiene_profesor:
                    todas_materias_con_profesores = False
            cursos_con_materias_y_profesores[curso]=[cantidad_alumnos_por_curso, todas_materias_con_profesores]
            
            
        print(cursos_con_materias_y_profesores)
        context['cursos_con_materias_y_profesores'] = cursos_con_materias_y_profesores
        context['active_tab'] = "cursos"
        return context
    
class CursoDeleteView(MultipleRolesRequiredMixin,SuccessMessageMixin, DeleteView):
    model = Curso
    success_url = reverse_lazy('cursos:ver_cursos')  # Redirigir al listado de planes de estudio
    success_message = "El curso %(nombre) ha sido eliminado exitosamente."
    required_roles = ['STAFF', 'ADMINISTRADOR']


      # Sobrescribir el método delete para hacer la eliminación lógica
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.enabled = False  # Cambiar el estado a deshabilitado (eliminación lógica)
        self.object.save()  # Guardar los cambios en la base de datos
        return redirect(self.success_url)

    # Modificar el mensaje de éxito
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
 
 
class AlumnosCursoUpdateView(MultipleRolesRequiredMixin,TemplateView):
    template_name='cursos/cursos/modificar_alumnos_curso.html' 
    success_url = reverse_lazy('home')
    required_roles = ['STAFF', 'ADMINISTRADOR']

    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        curso = Curso.objects.get(pk=self.kwargs['pk'])
        dni_cursantes=list(Cursante.objects.filter(curso=curso).values_list('dni', flat=True))
       
        alumnos=persona.objects.filter(dni__in=dni_cursantes).using('id8')
        context['alumnos']=alumnos
        context['curso']=curso
        return  context
    
    def post(self, request, *args, **kwargs):

        # Obtener los alumnos seleccionados del request
        alumnos = request.POST.get('alumnos_seleccionados')
        try:
            alumnos_seleccionados = json.loads(alumnos)
        except json.JSONDecodeError:
            alumnos_seleccionados = []

        curso = self.get_context_data().get('curso')  # Curso no guardado aún
        
        # Empezar una transacción
        with transaction.atomic():
            try:
                # Primero, obtener todos los Cursante existentes para el curso
                cursantes_existentes = Cursante.objects.filter(curso=curso, activo=True)

                # Ahora eliminar los cursantes que no están en la lista seleccionada
                for cursante in cursantes_existentes:
                    if str(cursante.dni) not in alumnos_seleccionados:
                        cursante.delete()
                        messages.warning(request, f'Cursante con DNI {cursante.dni} eliminado.')
                # Crear o actualizar Cursantes
                for alumno_dni in alumnos_seleccionados:
                    # Intentar obtener o crear el cursante
                    cursante, created = Cursante.objects.get_or_create(dni=int(alumno_dni), curso=curso)
                    if created:
                        # Mensaje opcional si se crea un nuevo cursante
                        messages.info(request, f'Cursante con DNI {alumno_dni} creado.')

                

                # Guardar el curso después de asociar todos los alumnos
                curso.save(request=request)  # Pasamos el request para almacenar el usuario que realizó el cambio
                # Mensaje de éxito
                messages.success(request, 'El curso se ha actualizado y se han asociado los alumnos correctamente.')
                
            except IntegrityError as e:
                # Manejar errores de integridad (como el nombre del curso duplicado)
                messages.error(request, 'El nombre del curso ya existe. Por favor, elige otro.')
                return self.form_invalid(self.get_form())
            except Exception as e:
                # Si ocurre un error, la transacción se revertirá
                messages.error(request, f'Hubo un error al asociar los alumnos: {str(e)}')
                return self.form_invalid(self.get_form())
 
            # Redirigir a la URL de éxito después de agregar el mensaje
            return redirect(reverse_lazy('cursos:ver_cursos'))
 
 
 
    
class AsignarProfesores(MultipleRolesRequiredMixin,ListView):
    model=Materia
    template_name='cursos/materias/asignar_profesores.html'
    context_object_name='materias'
    required_roles = ['STAFF', 'ADMINISTRADOR']
   

    def get_queryset(self):
        curso_id=self.kwargs.get('pk')
        curso = Curso.objects.get(id=curso_id)
        materias = Materia.objects.filter(materias_plan_de_estudio=curso.plan_de_estudio).prefetch_related(
                Prefetch('profesor_materia', queryset=Profesor.objects.filter(curso=curso))
                    )
        
        return materias

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curso = Curso.objects.get(pk=self.kwargs['pk'])
        #materias = curso.plan_de_estudio.materias.all()


        materias = Materia.objects.filter(materias_plan_de_estudio=curso.plan_de_estudio).prefetch_related(
                Prefetch('profesor_materia', queryset=Profesor.objects.filter(curso=curso))
                    )
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
            print(curso, "CUROOOOOSSS")
            # Eliminar las asignaciones existentes para usuarios deseleccionados
            # Eliminar las asignaciones existentes para usuarios deseleccionados de forma más eficiente
            
           # Obtener los profesores que coinciden con los usuarios deseleccionados
            profesores = Profesor.objects.filter(usuario__usuario__in=usuarios_deseleccionados, curso=curso)

            # Iterar sobre los profesores y remover la materia de cada uno
            for profesor in profesores:
                profesor.materias.remove(materia)  # Esto desasigna la materia del profesor


                messages.warning(request, f'Se ha eliminado la asignación del profesor {profesor.usuario} para este curso y materia.')
           
             
            # Crear o actualizar las nuevas asignaciones
             # Crear o actualizar las nuevas asignaciones
            for usuario in usuarios_seleccionados:
                perfil = usuario.perfil
                # Crear o recuperar el profesor sin el campo ManyToMany
                profesor, created = Profesor.objects.get_or_create(usuario=perfil)
                
                # Añadir el curso y la materia al profesor
                profesor.curso.add(curso)  # Relacionar con el curso
                profesor.materias.add(materia)  # Relacionar con la materia

                if created:
                    messages.success(request, f'El profesor {perfil} ha sido creado y asignado correctamente.')
                else:
                    messages.success(request, f'El profesor {perfil} ha sido asignado correctamente.')

        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
            context['form'] = form
            return self.render_to_response(context)

        # Redirigir pasando los ids de curso y materia
        return redirect(reverse_lazy('cursos:asignar_profesores', kwargs={'pk': curso.id}))
    
    
    
class VerFechasMaterias(TemplateView):
        template_name = "cursos/materias/ver_fechas.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            anio_lectivo=datetime.date.today().year
            
            '''
            Definimos como contexto las fechas de las materias.
            para cada régimen de materia, creamos un diccionario, cuya clave es el subperiodo y el valor es la fecha correspondiente
            '''
            aplica_para_opciones=("TODOS", "1","2", "3")
            
            for aplica_para in aplica_para_opciones:
               
                fechas_anuales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="ANUAL", aplica_para=aplica_para)
                fechas_anuales={}
                for fecha in fechas_anuales_registradas:
                    if fecha.subPeriodo:
                        fechas_anuales[fecha.subPeriodo]=fecha.fechaTopeCalificacion

                fechas_semestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL", aplica_para=aplica_para)
                fechas_semestrales={}
                for fecha in fechas_semestrales_registradas:
                    if fecha.subPeriodo:
                        fechas_semestrales[fecha.subPeriodo]=fecha.fechaTopeCalificacion
                
                fechas_cuatrimestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL", aplica_para=aplica_para)
                fechas_cuatrimestrales={}
                for fecha in fechas_cuatrimestrales_registradas:
                    if fecha.subPeriodo:
                        fechas_cuatrimestrales[fecha.subPeriodo]=fecha.fechaTopeCalificacion
                
                fechas_trimestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL", aplica_para=aplica_para)
                fechas_trimestrales={}
                for fecha in fechas_trimestrales_registradas:
                    if fecha.subPeriodo:
                        fechas_trimestrales[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            
                context[f"fechas_anuales_{aplica_para}"] =fechas_anuales
                context[f"fechas_semestrales_{aplica_para}"] =fechas_semestrales 
                context[f"fechas_cuatrimestrales_{aplica_para}"] =fechas_cuatrimestrales 
                context[f"fechas_trimestrales_{aplica_para}"] =fechas_trimestrales 
            return context
        
 
class DefinirFechas(MultipleRolesRequiredMixin,TemplateView):
    template_name='cursos/materias/definir_fechas.html'
    required_roles = ['STAFF', 'ADMINISTRADOR']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=FechasCreateForm()
        
        return context
    
    def post(self, request, *args: str, **kwargs):
        
        form=FechasCreateForm(request.POST)  
        anio_lectivo=datetime.date.today().year   
        actualizado=[]
        creado=[]
        
        if form.is_valid():      
            data=form.cleaned_data
            aplica_para = data.get('aplica_para', "TODOS")
            print(data['aplica_para'])
            fecha_inicio_ciclo_lectivo=(data['fecha_inicio_ciclo_lectivo'])
            
            '''Definción de trimestres para anuales, trimestrales y semestrales'''
            if data['T1']:
                anual_T1, an_t1_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="ANUAL", subPeriodo='T1',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':fecha_inicio_ciclo_lectivo,
                'fechaTopeCalificacion':data['T1']})
                anual_T1.fechaInicioCalificacion=fecha_inicio_ciclo_lectivo
                anual_T1.fechaTopeCalificacion=data['T1']  
                anual_T1.save()     
                
                semestre_T1, sem_t1_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL", subPeriodo='T1',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':fecha_inicio_ciclo_lectivo,
                'fechaTopeCalificacion':data['T1']})
                semestre_T1.fechaInicioCalificacion=fecha_inicio_ciclo_lectivo
                semestre_T1.fechaTopeCalificacion=data['T1']
                semestre_T1.save()
                
                trimestre_T1, tri_t1_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL", subPeriodo='T1',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':fecha_inicio_ciclo_lectivo,
                'fechaTopeCalificacion':data['T1']})
                trimestre_T1.fechaInicioCalificacion=fecha_inicio_ciclo_lectivo
                trimestre_T1.fechaTopeCalificacion=data['T1']
                trimestre_T1.save()
                if an_t1_created and tri_t1_created and sem_t1_created:
                    creado.append("Primer Trimestre")
                else:
                    actualizado.append('Primer Trimestre')
                
                
            if data['T2'] :
                if data['T1']:
                    anual_T1, an_t2_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="ANUAL", subPeriodo='T2',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T1'],
                    'fechaTopeCalificacion':data['T2']})
                    anual_T1.fechaInicioCalificacion=data['T1']
                    anual_T1.fechaTopeCalificacion=data['T2']  
                    anual_T1.save()  
                    
                    semestre_T2, sem_t2_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL", subPeriodo='T2',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T1'],
                    'fechaTopeCalificacion':data['T2']})
                    semestre_T2.fechaInicioCalificacion=data['T1']
                    semestre_T2.fechaTopeCalificacion=data['T2']
                    semestre_T2.save() 
                    
                    trimestre_T2, tri_t2_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL", subPeriodo='T2',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T1'],
                    'fechaTopeCalificacion':data['T2']})
                    trimestre_T2.fechaInicioCalificacion=data['T1']
                    trimestre_T2.fechaTopeCalificacion=data['T2']
                    trimestre_T2.save() 
                    if an_t2_created and tri_t2_created and sem_t2_created:
                        creado.append("Segundo Trimestre")
                    else:
                        actualizado.append("Segundo Trimestre")
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 1° Trimestre, para definir el 2° Trimestre")
                
            if data['T3'] :
                if data['T2']:
                    anual_T1, an_t3_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="ANUAL", subPeriodo='T3',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T2'],
                    'fechaTopeCalificacion':data['T3']})
                    anual_T1.fechaInicioCalificacion=data['T2']
                    anual_T1.fechaTopeCalificacion=data['T3']  
                    anual_T1.save()  
                    
                    semestre_T3, sem_t3_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL", subPeriodo='T3',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T2'],
                    'fechaTopeCalificacion':data['T3']})
                    semestre_T3.fechaInicioCalificacion=data['T2']
                    semestre_T3.fechaTopeCalificacion=data['T3']
                    semestre_T3.save()  
                    
                    trimestre_T3, tri_t3_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL", subPeriodo='T3',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T2'],
                    'fechaTopeCalificacion':data['T3']})
                    trimestre_T3.fechaInicioCalificacion=data['T2']
                    trimestre_T3.fechaTopeCalificacion=data['T3']
                    trimestre_T3.save()
                    if an_t3_created and tri_t3_created and sem_t3_created:
                        creado.append("Tercer Trimestre")
                    else:    
                        actualizado.append("Tercer Trimestre")
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 2° Trimestre, para definir el 3° Trimestre")             
                
            if data['T4'] :
                if data['T3']:
                    anual_T1, an_t4_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="ANUAL", subPeriodo='T4',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T3'],
                    'fechaTopeCalificacion':data['T4']})
                    anual_T1.fechaInicioCalificacion=data['T3']
                    anual_T1.fechaTopeCalificacion=data['T4']  
                    anual_T1.save() 
                    
                    semestre_T4, sem_t4_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL", subPeriodo='T4',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T3'],
                    'fechaTopeCalificacion':data['T4']})
                    semestre_T4.fechaInicioCalificacion=data['T3']
                    semestre_T4.fechaTopeCalificacion=data['T4']
                    semestre_T4.save()  
                    
                    trimestre_T4, tri_t4_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL", subPeriodo='T4',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T3'],
                    'fechaTopeCalificacion':data['T4']})
                    trimestre_T4.fechaInicioCalificacion=data['T3']
                    trimestre_T4.fechaTopeCalificacion=data['T4']
                    trimestre_T4.save() 
                    if an_t4_created and tri_t4_created and sem_t4_created:
                        creado.append("Cuarto Trimestre")
                    else:    
                        actualizado.append("Cuarto Trimestre")  
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 3° Trimestre, para definir el 4° Trimestre")
                
                '''Finales Trimestrales'''
            if data['FT_1'] :
                if data['T1']:
                    final_1trimestral, ft1_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='TRIMESTRAL', subPeriodo='FT_1',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T1'],
                    'fechaTopeCalificacion':data['FT_1']})
                    final_1trimestral.save()
                    if ft1_created:
                        creado.append("Final Primer Trimestre")
                    else:
                        actualizado.append("Final Primer Trimestre")
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 1° Trimestre, para definir el período de finales del 1° Trimestre")
            if data['FT_2'] :
                if data['T2']:
                    final_2trimestral, ft2_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='TRIMESTRAL', subPeriodo='FT_2',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T2'],
                    'fechaTopeCalificacion':data['FT_2']})
                    final_2trimestral.save()
                    if ft2_created:
                        creado.append("Final Segundo Trimestre")
                    else:
                        actualizado.append("Final Segundo Trimestre")
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 2° Trimestre, para definir el período de finales del 2° Trimestre")
                    
            if data['FT_3'] :
                if data['T3']:
                    final_3trimestral, ft3_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='TRIMESTRAL', subPeriodo='FT_3',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T3'],
                    'fechaTopeCalificacion':data['FT_3']})
                    if ft3_created:
                        creado.append("Final Tercer Trimestre")
                    else:
                        actualizado.append("Final Tercer Trimestre")
                    final_3trimestral.save()
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 3° Trimestre, para definir el período de finales del 3° Trimestre")
                    
            if data['FT_4'] :
                if data['T4']:
                    final_4trimestral, ft4_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='TRIMESTRAL', subPeriodo='FT_4',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T4'],
                    'fechaTopeCalificacion':data['FT_4']})
                    if ft4_created:
                        creado.append("Final Cuarto Trimestre")
                    else:
                        actualizado.append("Final Cuarto Trimestre")
                    final_4trimestral.save()
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del 4° Trimestre, para definir el período de finales del 4° Trimestre")
                    
                    
                    #Finales Semestrales         
            if data['FS_A']:
                if data['T2']:
                    final_semestre_A, fs_a_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='SEMESTRAL', subPeriodo='FS_A',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T2'],
                    'fechaTopeCalificacion':data['FS_A']})
                    if fs_a_created:
                        creado.append("Final Primer Semestre")
                    else:
                        actualizado.append("Final Primer Semestre")
                    final_semestre_A.save()
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Segundo Trimestre, para definir el período de finales Semestrales (1° Semestre)")
            if data['FS_B']:
                if data['T4']:
                    final_semestre_B, fs_b_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='SEMESTRAL', subPeriodo='FS_B', aplica_para=aplica_para,defaults={'fechaInicioCalificacion':data['T4'],
                    'fechaTopeCalificacion':data['FS_B']})
                    if fs_b_created:
                        creado.append("Final Segundo Semestre")
                    else:
                        actualizado.append("Final Segundor Semestre")
                    final_semestre_B.save()
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Cuarto Trimestre, para definir el período de finales Semestrales (2° Semestre)")
                    
            
            #finales anuales
            if data['FA']:
                if data['T4']:
                    final_anual, fa_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='ANUAL', subPeriodo='FA',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['T4'],
                    'fechaTopeCalificacion':data['FA']})
                    final_anual.fechaInicioCalificacion=data['T4']
                    final_anual.fechaTopeCalificacion=data['FA']
                    if fa_created:
                        creado.append("Final Anual")
                    else:
                        actualizado.append("Final Anual")
                    final_anual.save()
                    
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Cuarto Trimestre, para definir el periódo de exámenes finales Anuales")
            
            
            #definición de bimestres:
            if data['B1_A']:
                bimestre1_A, b1_a_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL", subPeriodo='B1_A',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':fecha_inicio_ciclo_lectivo,
                'fechaTopeCalificacion':data['B1_A']})
                bimestre1_A.fechaInicioCalificacion=fecha_inicio_ciclo_lectivo
                bimestre1_A.fechaTopeCalificacion=data['B1_A']  
                if b1_a_created:
                        creado.append("Primer Bimestre - Primer Cuatrimestre")
                else:
                    actualizado.append("Primer Bimestre - Primer Cuatrimestre")
                bimestre1_A.save()  
                
                
            if data['B2_A']:
                if data['B1_A']:
                    bimestre2_A, b2_a_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL", subPeriodo='B2_A',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['B1_A'],
                    'fechaTopeCalificacion':data['B2_A']})
                    bimestre2_A.fechaInicioCalificacion=data['B1_A']
                    bimestre2_A.fechaTopeCalificacion=data['B2_A'] 
                    if b2_a_created:
                            creado.append("Segundo Bimestre - Primer Cuatrimestre")
                    else:
                        actualizado.append("Segundo Bimestre - Primer Cuatrimestre") 
                    bimestre2_A.save()    
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Primer Bimestre, para definir el segundo bimestre (1° Cuatrimestre)")
              

            if data['B1_B']:
                if data['B2_A']:
                    bimestre1_B, b1_b_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL", subPeriodo='B1_B',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['B2_A'],
                    'fechaTopeCalificacion':data['B1_B']})
                    bimestre1_B.fechaInicioCalificacion=data['B2_A']
                    bimestre1_B.fechaTopeCalificacion=data['B1_A']  
                    if b1_b_created:
                            creado.append("Primer Bimestre - Segundo Cuatrimestre")
                    else:
                        actualizado.append("Primer Bimestre - Segundo Cuatrimestre")
                    bimestre1_B.save()
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Primer Cuatrimestre, para definir el primer bimestre (2° Cuatrimestre)")
              

                
            if data['B2_B']:
                if data['B1_B']:
                    bimestre1_B, b2_b_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL", subPeriodo='B2_B',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['B1_B'],
                    'fechaTopeCalificacion':data['B2_B']})
                    bimestre1_B.fechaInicioCalificacion=data['B1_B']
                    bimestre1_B.fechaTopeCalificacion=data['B2_B'] 
                    if b2_b_created:
                            creado.append("Segundo Bimestre - Segundo Cuatrimestre")
                    else:
                        actualizado.append("Segundo Bimestre - Segundo Cuatrimestre")  
                    bimestre1_B.save()
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Primer Bimestre, para definir el segundo bimestre (2° Cuatrimestre)")

      
                
                
        #       FINALES CUATRIMESTRALES
            if data['FC_A']:
                if data['B2_A']:
                    final_cuatrimestre_A, fc_a_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='CUATRIMESTRAL', subPeriodo='FC_A',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['B2_A'],
                    'fechaTopeCalificacion':data['FC_A']})
                    final_cuatrimestre_A.fechaInicioCalificacion=data['B2_A']
                    final_cuatrimestre_A.fechaTopeCalificacion=data['FC_A']
                    if fc_a_created:
                        creado.append("Final Primer Cuatrimestre")
                    else:
                        actualizado.append("Final Primer Cuatrimestre") 
                    final_cuatrimestre_A.save()
                else:
                    print("falta el fin del segundo bimestre")
                    messages.error(request, "Es necesario fijar previamente el fin del Segundo Bimestre, para definir el período de finales del Primer Cuatrimestre")
                    
                    
            if data['FC_B']:
                if data['B2_B']:
                    final_cuatrimestre_B, fc_b_created=FechasExamenes.objects.get_or_create(anio_lectivo=anio_lectivo, regimen_materia='CUATRIMESTRAL', subPeriodo='FC_B',aplica_para=aplica_para, defaults={'fechaInicioCalificacion':data['B2_B'],
                    'fechaTopeCalificacion':data['FC_B']})
                    final_cuatrimestre_B.fechaInicioCalificacion=data['B2_B']
                    final_cuatrimestre_B.fechaTopeCalificacion=data['FC_B']
                    final_cuatrimestre_B.save()
                    if fc_b_created:
                        creado.append("Final Segundo Cuatrimestre")
                    else:
                        actualizado.append("Final Segundo Cuatrimestre")
                    final_cuatrimestre_A.save()
                    
                else:
                    messages.error(request, "Es necesario fijar previamente el fin del Segundo Bimestre, para definir el período de finales del segundo Cuatrimestre")
           
            if creado !=[]:
                mensaje_creacion=f'Se han definido correctamente las siguientes fechas: {', '.join(creado)}'
                messages.success(request, mensaje_creacion)    

            if actualizado!=[]:
                mensaje_actualizacion=f'Se han actualizado correctamente las siguientes fechas {', '.join(actualizado)}'
                messages.success(request, mensaje_actualizacion)
            '''
            anual_T1= Primer trimestre, inicia con el inicio del ciclo académico
            anual_T2=Segundo trimestre, inicia con el fin del 1T
            anual_T3=Tercer Trimestre, Inicia con el fin del 2T
            anual_T4=Cuarto Trimestre, inicia con el fin del 3T. Cierre de Cursada
            FA=Final anual, inicia con el cierre de cursada
            
            semestralesA_T1=Primer trimestre, inicia con el ciclo ocadémico, coincide con el anual_t1
            semestralesA_T2=Segudo Trimestre, inicia con el fin del 1 trimestre
            FSA=Final semestral, inicia con el fin del Semestre 2
            semestralesB_T1= idem al anterior, pero inica con el fin del semestre 2
            semestralesB_T2= idem al anterios, pero en el segundo semestre del año
            FSB= idem al anterios, pero en el segundo semestre del año
            
            T1= igual a los trimestres anuales
            T2= igual a los trimestres anuales
            T3= igual a los trimestres anuales
            T4= igual a los trimestres anuales
            FT1= Final del trimestre, inicia con el final de T correspondiente
            FT2= Final del trimestre, inicia con el final de T correspondiente
            FT3= Final del trimestre, inicia con el final de T correspondiente
            FT4= Final del trimestre, inicia con el final de T correspondiente
            
            B1_A=Primer bimestre del cuatrimestre, inicia con el ciclo lectivo
            B2_A= segundo bimestres del cuatrimestre, inicia con el fin del bimestre 1
            FC_A= final del cuatrimestre, inicia con el fin del cuatrimestre 2
            B1_B=Primer bimestre del cuatrimestre, inica con el fin del segundo bimestre del cuatrimestre 
            B2_B=idem al bimestre 2_a, pero para la segunda mitad de año
            FC_B=final del cuatrimestre, inicia con el fin del cuatrimestre 2_b.
            '''
            
         
        return redirect(reverse_lazy('cursos:definir_fechas'))



class update_fechas(UpdateView):
    pass





#

def fijarInicioAnioLectivo(request):
    if request.method == "POST":
        fecha_inicio_ciclo_lectivo = request.POST.get('fecha_inicio_ciclo_lectivo')
        
        # Verifica que la fecha de inicio no sea vacía
        if not fecha_inicio_ciclo_lectivo:
            # Maneja el caso en que no se proporciona una fecha
            return redirect('cursos:definir_fechas')

        print(fecha_inicio_ciclo_lectivo)

        # Lista de tipos de regimen y subperiodo
        tipos = [
            ("ANUAL", "1T"),
            ("SEMESTRAL", "1T_A"),
            ("CUATRIMESTRAL", "1B_A"),
            ("TRIMESTRAL", "1T"),
        ]

        for regimen, sub_periodo in tipos:
            # Intentamos obtener la instancia
            try:
                fechas = FechasExamenes.objects.get(
                    anio_lectivo=datetime.date.today().year,
                    regimen_materia=regimen,
                    subPeriodo=sub_periodo,
                )
                # Si la instancia ya existía, actualiza el campo
                fechas.fechaInicioCalificacion = fecha_inicio_ciclo_lectivo
                fechas.save()
            except ObjectDoesNotExist:
                # Si no existe, crea una nueva instancia
                FechasExamenes.objects.create(
                    anio_lectivo=datetime.date.today().year,
                    regimen_materia=regimen,
                    subPeriodo=sub_periodo,
                    fechaInicioCalificacion=fecha_inicio_ciclo_lectivo,
                )

        return redirect('cursos:definir_fechas')

    return redirect('cursos:definir_fechas')

