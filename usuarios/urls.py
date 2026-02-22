from django.urls import path
from . import views

app_name = 'usuarios'  # ← ESTO ES OBLIGATORIO

urlpatterns = [
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('lista-residentes/', views.lista_residentes, name='lista_residentes'),
    # Agrega otras rutas si quieres (ej: editar, listar usuarios)
]