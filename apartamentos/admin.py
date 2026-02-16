from django.contrib import admin
from .models import Apartamento


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = (
        'identificador',
        'bloque_o_torre',
        'piso',
        'estado',
        'ocupante_actual',
        'area_m2',
    )
    list_display_links = ('identificador',)          # clic en este campo abre el detalle
    list_filter = ('estado', 'bloque_o_torre')
    search_fields = (
        'identificador',
        'bloque_o_torre',
        'ocupante_actual__username',
        'ocupante_actual__first_name',
        'ocupante_actual__last_name',
        'ocupante_actual__documento',
    )
    list_select_related = ('ocupante_actual',)       # optimiza consultas cuando hay FK
    ordering = ['identificador']                     # ya no usamos torre/numero
    readonly_fields = ('creado_en', 'actualizado_en')

    fieldsets = (
        ('Información básica', {
            'fields': ('identificador', 'bloque_o_torre', 'piso', 'area_m2')
        }),
        ('Estado y ocupación', {
            'fields': ('estado', 'ocupante_actual'),
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',),
        }),
        ('Metadatos', {
            'fields': ('creado_en', 'actualizado_en'),
            'classes': ('collapse',),
        }),
    )