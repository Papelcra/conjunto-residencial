from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_lista_anuncios, name="admin_lista_anuncios"),
    path("crear/", views.crear_anuncio, name="crear_anuncio"),
    path("editar/<int:pk>/", views.editar_anuncio, name="editar_anuncio"),
    path("eliminar/<int:pk>/", views.eliminar_anuncio, name="eliminar_anuncio"),
]