from django.urls import path
from . import views

app_name = 'usuarios'  # ← ESTO ES OBLIGATORIO

urlpatterns = [
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('lista-residentes/', views.lista_residentes, name='lista_residentes'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('solicitudes-recuperacion/', views.solicitudes_recuperacion, name='solicitudes_recuperacion'),
]