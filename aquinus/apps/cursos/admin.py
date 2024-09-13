from django.contrib import admin
from .models import Materia, PlanEstudio, Cursante, Curso, Calificaciones
# Register your models here.
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display=['nombre','abreviatura','tipo']
    
@admin.register(PlanEstudio)
class PlanEstudioAdmin(admin.ModelAdmin):
    list_display=['especialidad', 'anio','vigente']
    
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display=['nombre', 'plan_de_estudio','activo', 'puede_calificar']
    list_display=['plan_de_estudio']
    
@admin.register(Cursante)
class CursanteAdmin(admin.ModelAdmin):
    list_display=['dni', 'curso']
    raw_id_fields=[ 'curso']
    
@admin.register(Calificaciones)
class CalificacionesAdmin(admin.ModelAdmin):
    list_display=['materia', 'cursante', 'valor', 'tipo']
    raw_id_fields=['materia', 'cursante']