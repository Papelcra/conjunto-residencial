from django.urls import path
from . import views

app_name = "zonas"

urlpatterns = [
    path("reservar/", views.crear_reserva, name="crear"),
    path("calendario/", views.calendario_reservas, name="calendario"),
    path("crear-zona/", views.crear_zona, name="crear_zona"),
]