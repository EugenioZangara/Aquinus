import datetime
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="materias"   
        return context
       
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="planes_estudio"   
        return context
    

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="planes_estudio"   
        return context
    
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
    
class CursoDeleteView(SuccessMessageMixin, DeleteView):
    model = Curso
    success_url = reverse_lazy('cursos:ver_cursos')  # Redirigir al listado de planes de estudio
    success_message = "El curso %(nombre) ha sido eliminado exitosamente."


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
 
 
class AlumnosCursoUpdateView(TemplateView):
    template_name='cursos/cursos/modificar_alumnos_curso.html' 
    success_url = reverse_lazy('home')

    
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
 
 
 
    
class AsignarProfesores(ListView):
    model=Materia
    template_name='cursos/materias/asignar_profesores.html'
    context_object_name='materias'
    

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
            fechas_anuales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="ANUAL")
            fechas_anuales={}
            for fecha in fechas_anuales_registradas:
                if fecha.subPeriodo:
                    fechas_anuales[fecha.subPeriodo]=fecha.fechaTopeCalificacion

            fechas_semestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="SEMESTRAL")
            fechas_semestrales={}
            for fecha in fechas_semestrales_registradas:
                if fecha.subPeriodo:
                    fechas_semestrales[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            
            fechas_cuatrimestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="CUATRIMESTRAL")
            fechas_cuatrimestrales={}
            for fecha in fechas_cuatrimestrales_registradas:
                if fecha.subPeriodo:
                    fechas_cuatrimestrales[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            
            fechas_trimestrales_registradas=FechasExamenes.objects.filter(anio_lectivo=anio_lectivo, regimen_materia="TRIMESTRAL")
            fechas_trimestrales={}
            for fecha in fechas_trimestrales_registradas:
                if fecha.subPeriodo:
                    fechas_trimestrales[fecha.subPeriodo]=fecha.fechaTopeCalificacion
            
            context["fechas_anuales"] =fechas_anuales
            context["fechas_semestrales"] =fechas_semestrales 
            context["fechas_cuatrimestrales"] =fechas_cuatrimestrales 
            context["fechas_trimestrales"] =fechas_trimestrales 
            return context
        
 
class DefinirFechas(TemplateView):
    template_name='cursos/materias/definir_fechas.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificamos si existe una fecha de inicio de ciclo lectivo definida.
        
        fechaAnual = FechasExamenes.objects.filter(anio_lectivo=datetime.date.today().year, regimen_materia="ANUAL", subPeriodo="1T").values_list('fechaInicioCalificacion', flat=True)
        fechaSemestral = FechasExamenes.objects.filter(anio_lectivo=datetime.date.today().year, regimen_materia="SEMESTRAL", subPeriodo="1T_A").values_list('fechaInicioCalificacion', flat=True)
        fechaCuatrimestrales = FechasExamenes.objects.filter(anio_lectivo=datetime.date.today().year, regimen_materia="CUATRIMESTRAL", subPeriodo="1B_A").values_list('fechaInicioCalificacion', flat=True)
        fechasTrimestrales = FechasExamenes.objects.filter(anio_lectivo=datetime.date.today().year, regimen_materia="TRIMESTRAL", subPeriodo="1T").values_list('fechaInicioCalificacion', flat=True)

        fecha_inicio_ciclo_lectivo = None
        mensaje_advertencia = ""

        # Crear un diccionario para almacenar los resultados
        fechas_existentes = {
            "Anual": list(fechaAnual),
            "Semestral": list(fechaSemestral),
            "Cuatrimestral": list(fechaCuatrimestrales),
            "Trimestral": list(fechasTrimestrales),
        }

        # Filtrar las que existen
        fechas_definidas = {materia: fechas for materia, fechas in fechas_existentes.items() if fechas}

        if fechas_definidas:
            # Extraer las fechas únicas y su correspondiente tipo
            fechas_unicas = {}
            for materia, fechas in fechas_definidas.items():
                for fecha in fechas:
                    fechas_unicas.setdefault(fecha, []).append(materia)

            # Verificar si hay más de una fecha única
            if len(fechas_unicas) > 1:
                # Crear un mensaje con las fechas distintas, convirtiéndolas a string
                fechas_distintas = ", ".join(sorted(f.strftime('%Y-%m-%d') for f in fechas_unicas.keys()))
                tipos = ", ".join(sorted(set(materia for materias in fechas_unicas.values() for materia in materias)))
                mensaje_advertencia = f"Advertencia: Existen diferentes fechas de inicio del ciclo lectivo: {fechas_distintas}. Tipos: {tipos}."
            else:
                mensaje_advertencia = "Ya existe una fecha de Inicio del ciclo lectivo, si la modifica, afectará el inicio de TODAS las materias."
                fecha_inicio_ciclo_lectivo = list(fechas_unicas.keys())[0]  # Obtener la fecha única

        context["fecha_default"] = fecha_inicio_ciclo_lectivo
        context['mensaje_advertencia'] = mensaje_advertencia
        context['form_anual'] = FechasCreateForm(regimen_materia="ANUAL")
        context["form_semestral"] = FechasCreateForm(regimen_materia="SEMESTRAL")
        context['form_cuatrimestral'] = FechasCreateForm(regimen_materia="CUATRIMESTRAL")
        context['form_trimestral'] = FechasCreateForm(regimen_materia="TRIMESTRAL")
        
        return context
    
    def post(self, request, *args: str, **kwargs):
        
        submit_button = request.POST.get('submit_button')
        if submit_button == 'inicio_ciclo_lectivo':
            print(request.POST)
        if submit_button == 'formulario_anuales':
            form=FechasCreateForm(regimen_materia="ANUAL",data=request.POST)
            
            if form.is_valid():      
                data=form.cleaned_data
                try:
                    if data['anual_primer_trimestre']:
                        anual_1T=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="ANUAL",
                                                    subPeriodo="1T",
                                                    fechaInicioCalificacion=data['fecha_inicio_ciclo_lectivo'],
                                                    fechaTopeCalificacion=data['anual_primer_trimestre']
                                                    )
                        anual_1T.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Primer Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                         f"para las materias Anuales")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="ANUAL",
                        subPeriodo="1T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                   f"para el Primer Trimestre de las materias Anuales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
              
                try:
                    if data['anual_segundo_trimestre']:
                        anual_2T=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="ANUAL",
                                                    subPeriodo="2T",
                                                    fechaInicioCalificacion=data['anual_primer_trimestre'],
                                                    fechaTopeCalificacion=data['anual_segundo_trimestre']
                                                    )
                        anual_2T.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Segundo Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                         f"para las materias Anuales")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="ANUAL",
                        subPeriodo="2T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                   f"para el Segundo Trimestre de las materias Anuales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                   
                    
                try:    
                    if data['anual_tercer_trimestre']:
                                                
                        anual_3T=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="ANUAL",
                                                    subPeriodo="3T",
                                                    fechaInicioCalificacion=data['anual_segundo_trimestre'],
                                                    fechaTopeCalificacion=data['anual_tercer_trimestre']
                                                    )
                        anual_3T.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Tercer Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                         f"para las materias Anuales")
                    else:
                        pass
                    
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=data['anio_lectivo'],
                        regimen_materia="ANUAL",
                        subPeriodo="3T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                   f"para el Tercer Trimestre de las materias Anuales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                try:    
                    if data['anual_cierre']:
                        anual_cierre=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="ANUAL",
                                                    subPeriodo="CIERRE_ANUAL",
                                                    fechaInicioCalificacion=data['anual_tercer_trimestre'],
                                                    fechaTopeCalificacion=data['anual_cierre']
                                                    )
                        anual_cierre.save()
                        messages.success(request, f"Se ha fijado la fecha tope para el cierre de calificaciones del {form.cleaned_data['anio_lectivo']},  "
                                         f"para las materias Anuales")
                    else:
                        pass
                    
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="ANUAL",
                        subPeriodo="CIERRE_ANUAL"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                        f"para el Cierre anual de las materias Anuales. "
                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                  
                    
                try:
                    if data['anual_examen_final']: 
                        anual_final=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="ANUAL",
                                                    subPeriodo="EXAMEN_FINAL",
                                                    fechaInicioCalificacion=data['anual_cierre'],
                                                    fechaTopeCalificacion=data['anual_examen_final']
                                                    )
                        anual_final.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones de Exámenes Finales del {form.cleaned_data['anio_lectivo']},  "
                                         f"para las materias Anuales")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="ANUAL",
                        subPeriodo="EXAMEN_FINAL"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                   f"para el cierre de exámenes finales de las materias Anuales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                 
                    
                    
                
            else:
                print(form.errors)
            
            
            #Materias SEMESTRALES
                
        if submit_button == 'formulario_semestrales':
            form=FechasCreateForm(regimen_materia="SEMESTRAL",data=request.POST)
            
            if form.is_valid():
                data=form.cleaned_data
                #Primer Semestre - primera mitad de año= "A"
                try:
                    if data['semestral_primer_trimestre_a']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="SEMESTRAL",
                                                    subPeriodo="1T_A",
                                                    fechaInicioCalificacion=data['fecha_inicio_ciclo_lectivo'],
                                                    fechaTopeCalificacion=data['semestral_primer_trimestre_a']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Primer Trimestres del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="1T_A"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Primer Trimestre de las materias Semestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                
                #Cierre cursada Semestral - primera mitad de año= "A"
                try:
                    if data['semestral_cierre_a']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="SEMESTRAL",
                                                    subPeriodo="2T_A",
                                                    fechaInicioCalificacion=data['semestral_primer_trimestre_a'],
                                                    fechaTopeCalificacion=data['semestral_cierre_a']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cierre de Cursada del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="2T_A"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cierre de Cursada de las materias Semestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                #finales Semestrales - primera mitad de año ="A"
                
                try:
                    if data['semestral_examen_final_a']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="SEMESTRAL",
                                                    subPeriodo="FS_A",
                                                    fechaInicioCalificacion=data['semestral_cierre_a'],
                                                    fechaTopeCalificacion=data['semestral_examen_final_a']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cierre de Cursada del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="2T_A"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cierre de Cursada de las materias Semestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                
                #Primer Semestre - sEGUNDA mitad de año= "B"
                try:
                    if data['semestral_primer_trimestre_b']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="SEMESTRAL",
                                                    subPeriodo="1T_B",
                                                    fechaInicioCalificacion=data['semestral_cierre_a'],
                                                    fechaTopeCalificacion=data['semestral_primer_trimestre_b']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Primer Trimestres del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="1T_B"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Primer Trimestre de las materias Semestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                
                #Cierre cursada Semestral - segunda mitad de año= "B"
                try:
                    if data['semestral_cierre_b']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="SEMESTRAL",
                                                    subPeriodo="2T_B",
                                                    fechaInicioCalificacion=data['semestral_primer_trimestre_b'],
                                                    fechaTopeCalificacion=data['semestral_cierre_b']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cierre de Cursada del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="2T_B"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cierre de Cursada de las materias Semestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                #finales Semestrales - Segunda mitad de año ="B"
                
                try:
                    if data['semestral_examen_final_b']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="SEMESTRAL",
                                                    subPeriodo="FS_B",
                                                    fechaInicioCalificacion=data['semestral_cierre_b'],
                                                    fechaTopeCalificacion=data['semestral_examen_final_b']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cierre de Cursada del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="2T_B"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cierre de Cursada de las materias Semestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                
                    
            else:
                print(form.errors)
                #fin de las semestrales
                
                #materias CUATRIMESTRALES
                
        if submit_button == 'formulario_cuatrimestrales':
            form=FechasCreateForm(regimen_materia="CUATRIMESTRAL",data=request.POST)      
     
            if form.is_valid():
                data=form.cleaned_data
                print(data)
                #Primer Bitrimestre - primera mitad de año= "A"
                try:
                    if data['cuatrimestral_primer_bimestre_a']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="CUATRIMESTRAL",
                                                    subPeriodo="1B_A",
                                                    fechaInicioCalificacion=data['fecha_inicio_ciclo_lectivo'],
                                                    fechaTopeCalificacion=data['cuatrimestral_primer_bimestre_a']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Primer Bimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Cuatrimestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="CUATRIMESTRAL",
                        subPeriodo="1B_A"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Primer Bimestre de las materias Cuatrimestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                
                #Cierre cursada Cuatrimestral - primera mitad de año= "A"
                try:
                    if data['cuatrimestral_cierre_a']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="CUATRIMESTRAL",
                                                    subPeriodo="2B_A",
                                                    fechaInicioCalificacion=data['cuatrimestral_primer_bimestre_a'],
                                                    fechaTopeCalificacion=data['cuatrimestral_cierre_a']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cierre de Cursada del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Cuatrimestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="CUATRIMESTRAL",
                        subPeriodo="2B_A"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cierre de Cursada de las materias Cuatrimestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                #finales Cuatrimestrales - primera mitad de año ="A"
                
                try:
                    if data['cuatrimestral_examen_final_a']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="CUATRIMESTRAL",
                                                    subPeriodo="FC_A",
                                                    fechaInicioCalificacion=data['cuatrimestral_cierre_a'],
                                                    fechaTopeCalificacion=data['cuatrimestral_examen_final_a']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Examenes Finales del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Cuatrimestrales, de la primera mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="CUATRIMESTRAL",
                        subPeriodo="FC_A"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Examen Final de las materias Cuatrimestrales de la primera mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                
                #Primer Semestre - sEGUNDA mitad de año= "B"
                try:
                    if data['cuatrimestral_primer_bimestre_b']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="CUATRIMESTRAL",
                                                    subPeriodo="1B_B",
                                                    fechaInicioCalificacion=data['cuatrimestral_cierre_a'],
                                                    fechaTopeCalificacion=data['cuatrimestral_primer_bimestre_b']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Primer Bimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Cuatrimestrales, de la segunda mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="CUATRIMESTRAL",
                        subPeriodo="1B_B"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Primer Bimestre de las materias Cuatrimestrales de la Segunda mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                
                #Cierre cursada Semestral - segunda mitad de año= "B"
                try:
                    if data['cuatrimestral_cierre_b']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="CUATRIMESTRAL",
                                                    subPeriodo="2B_B",
                                                    fechaInicioCalificacion=data['cuatrimestral_primer_bimestre_b'],
                                                    fechaTopeCalificacion=data['cuatrimestral_cierre_b']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cierre de Cursada del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Semestrales, de la segunda mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="SEMESTRAL",
                        subPeriodo="2B_B"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cierre de Cursada de las materias Cuatrimestrales de la segunda mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                #finales Semestrales - Segunda mitad de año ="B"
                
                try:
                    if data['cuatrimestral_examen_final_b']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="CUATRIMESTRAL",
                                                    subPeriodo="FC_B",
                                                    fechaInicioCalificacion=data['cuatrimestral_cierre_b'],
                                                    fechaTopeCalificacion=data['cuatrimestral_examen_final_b']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones de los Exámenes Finales {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Cuatrimestrales, de la segunda mitad de año")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="CUATRIMESTRAL",
                        subPeriodo="FC_B"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para los exámenes Finales de las materias Cuatrimestrales de la segunda mitad de año."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                
                
                    
            else:
                print(form.errors)
        #fin cuatrimestrales     
            
            
            #materias Trimestrales  
        if submit_button == 'formulario_trimestrales':
            form=FechasCreateForm(regimen_materia="TRIMESTRAL",data=request.POST)
            
            if form.is_valid():
                #Primer trimestre
                try:
                    if data['primer_trimestre_cierre']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="1T",
                                                    fechaInicioCalificacion=data['fecha_inicio_ciclo_lectivo'],
                                                    fechaTopeCalificacion=data['primer_trimestre_cierre']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Primer Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="1T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Primer Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                    #Finales Primer trimestre
                try:
                    if data['primer_trimestre_examen_final']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="FT1",
                                                    fechaInicioCalificacion=data['primer_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['primer_trimestre_examen_final']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones de los exámenes Finales Primer Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="FT1"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para los exámenes Finales del Primer Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                    ################################################################
                    #Segundo trimestre
                try:
                    if data['segundo_trimestre_cierre']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="2T",
                                                    fechaInicioCalificacion=data['primer_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['segundo_trimestre_cierre']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Segundo Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="2T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Segundo Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                    #Finales Segundo trimestre
                try:
                    if data['segundo_trimestre_examen_final']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="FT2",
                                                    fechaInicioCalificacion=data['segundo_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['segundo_trimestre_examen_final']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones de los exámenes Finales Segundo Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="FT2"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para los exámenes Finales del Segundo Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                    
                    #####################################################################################
                    #tercer Trimestre
                try:
                    if data['tercer_trimestre_cierre']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="3T",
                                                    fechaInicioCalificacion=data['segundo_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['tercer_trimestre_cierre']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Tercer Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="3T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Tercer Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                    #Finales Tercer trimestre
                try:
                    if data['tercer_trimestre_examen_final']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="FT3",
                                                    fechaInicioCalificacion=data['tercer_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['tercer_trimestre_examen_final']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones de los exámenes Finales Tercer Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="FT3"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para los exámenes Finales del Tercer Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.') 
                    
                    ##############################################################################
                    
                    #Cuarto Trimestre
                    
                
                try:
                    if data['cuarto_trimestre_cierre']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="4T",
                                                    fechaInicioCalificacion=data['tercer_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['cuarto_trimestre_cierre']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones del Cuarto Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="4T"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para el Cuarto Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')
                    
                    #Finales Cuarto trimestre
                try:
                    if data['cuarto_trimestre_examen_final']:
                        semestral_1T_a=FechasExamenes.objects.create(anio_lectivo=data['anio_lectivo'],
                                                    regimen_materia="TRIMESTRAL",
                                                    subPeriodo="FT4",
                                                    fechaInicioCalificacion=data['cuarto_trimestre_cierre'],
                                                    fechaTopeCalificacion=data['cuarto_trimestre_examen_final']
                                                    )
                        semestral_1T_a.save()
                        messages.success(request, f"Se ha fijado la fecha tope para las calificaciones de los exámenes Finales Cuarto Trimestre del {form.cleaned_data['anio_lectivo']},  "
                                        f"para las materias Trimestrales.")
                    else:
                        pass
                except IntegrityError:
                    existing_instance = FechasExamenes.objects.get(
                        anio_lectivo=form.cleaned_data['anio_lectivo'],
                        regimen_materia="TRIMESTRAL",
                        subPeriodo="FT4"
                    )
                    update_url = reverse('cursos:update_fechas', kwargs={'pk': existing_instance.pk})
                    messages.error(request, f"Ya existe una fecha definida para el año lectivo {form.cleaned_data['anio_lectivo']}, "
                                f"para los exámenes Finales del Cuarto Trimestre de las materias Trimestrales."
                                        f'<a href="{update_url}">Haz clic aquí para editar</a>.')     
                    
            else:
                print(form.errors)
                
    
        return redirect(reverse_lazy('cursos:definir_fechas'))



class update_fechas(UpdateView):
    pass





from django.shortcuts import redirect
import datetime
from .models import FechasExamenes

from django.shortcuts import redirect
import datetime
from .models import FechasExamenes

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

