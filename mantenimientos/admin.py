from django.contrib import admin
from .models import Mantenimiento


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "apartamento", "residente", "estado", "fecha_solicitud")
    list_filter = ("estado",)
    search_fields = ("titulo", "descripcion", "apartamento__numero", "residente__username")
    ordering = ("-fecha_solicitud",)