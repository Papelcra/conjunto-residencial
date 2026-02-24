from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("crear/", views.crear_usuario, name="crear_usuario"),
    path("panel/", views.panel_residente, name="panel_residente"),
]
