from django.urls import path
from . import views

app_name = 'usuarios'  # ← ESTO ES OBLIGATORIO

urlpatterns = [
    path('crear/', views.crear_usuario, name='crear_usuario'),
    # Agrega otras rutas si quieres (ej: editar, listar usuarios)
]