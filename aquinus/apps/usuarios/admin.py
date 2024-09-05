from django.contrib import admin
from .models import Perfil
# Register your models here.
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display=['usuario','es_profesor', 'puede_calificar','activo']
    raw_id_fields = ['usuario']