from django.contrib import admin
from .models import Oportunidad

@admin.register(Oportunidad)
class OportunidadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'valor_estimado', 'etapa', 'fecha_creacion', 'fecha_cierre', 'dias_abierta')
    list_filter = ('etapa', 'fecha_cierre', 'fecha_creacion')
    search_fields = ('titulo', 'cliente__nombre')

