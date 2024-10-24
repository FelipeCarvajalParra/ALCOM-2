from django.contrib import admin
from .models import Referencias

class ReferenciasAdmin(admin.ModelAdmin):
    list_display = ('referencia_pk', 'categoria', 'marca', 'accesorios', 'observaciones', 'url_consulta')
    search_fields = ('referencia_pk', 'marca', 'observaciones')
    list_filter = ('categoria', 'marca')
    ordering = ('referencia_pk',)

admin.site.register(Referencias, ReferenciasAdmin)
