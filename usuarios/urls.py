from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_usuario, name="crear_usuario"),
    path("lista/", views.lista_usuarios, name="lista_usuarios"),
]
