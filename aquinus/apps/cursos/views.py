from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Materia
from django.views.generic import CreateView, ListView, DeleteView
from .forms import MateriaForm
# Create your views here.

class MateriaCreateView(CreateView):
    form_class = MateriaForm
    template_name = "cursos/crear_materia.html"
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
    template_name = "cursos/ver_materias.html"
    context_object_name = 'materias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab']="materias"   
        return context
    
class MateriaDeleteView(DeleteView):
    model = Materia
    success_url = reverse_lazy('cursos:ver_materias')  # Redirigir a la lista de materias después de eliminar
    