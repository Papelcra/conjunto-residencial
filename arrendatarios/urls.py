from django.urls import path
from . import views

app_name = "arrendatarios"

urlpatterns = [
    path("lista/", views.lista_arrendatarios, name="lista"),
    path("crear/", views.crear_arrendatario, name="crear"),
    path("editar/<int:id>/", views.editar_arrendatario, name="editar"),
    path("eliminar/<int:id>/", views.eliminar_arrendatario, name="eliminar"),

]
