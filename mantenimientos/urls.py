from django.urls import path
from . import views

app_name = "mantenimientos"

urlpatterns = [
    # Residente
    path("mis/", views.residente_lista, name="mis"),
    path("crear/", views.residente_crear, name="crear"),

    # Admin
    path("admin/", views.admin_lista, name="admin_lista"),
    path("admin/<int:pk>/", views.admin_editar, name="admin_editar"),
]