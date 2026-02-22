from django.contrib import admin
from .models import ZonaComun, Horario, Reserva

@admin.register(ZonaComun)
class ZonaComunAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'disponible')
    search_fields = ('nombre',)

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('zona', 'dia_semana', 'hora_inicio', 'hora_fin')
    search_fields = ('zona__nombre',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('residente', 'horario', 'fecha', 'estado')
    search_fields = ('residente__username', 'horario__zona__nombre')
    list_filter = ('estado', 'fecha')