from django.urls import path
from . import views

app_name = "pqrs"

urlpatterns = [
    # Rutas actuales y funcionales
    path('admin/', views.listar_pqrs, name='listar_pqrs'),
    path('crear/', views.crear_pqrs, name='crear_pqrs'),
    path('responder/<int:id>/', views.responder_pqrs, name='responder_pqrs'),
    path('mis/', views.mis_pqrs, name='mis_pqrs'),
    path('eliminar/<int:id>/', views.eliminar_pqrs, name='eliminar_pqrs'),

    # rutas futuras de pqrs (de develop - por ahora vacío)
]