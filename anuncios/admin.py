from django.contrib import admin
from .models import Anuncio

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion', 'destacado')
    list_filter = ('destacado',)
    search_fields = ('titulo',)