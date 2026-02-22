from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.lista_zonas, name='lista_zonas'),  # Lista de zonas comunes
    path('reservar/<int:horario_id>/', views.reservar, name='reservar'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('validar/', views.validar_reservas, name='validar_reservas'),
    path('aprobar/<int:reserva_id>/', views.aprobar_reserva, name='aprobar_reserva'),
    path('rechazar/<int:reserva_id>/', views.rechazar_reserva, name='rechazar_reserva'),
    path('gestionar-zonas/', views.gestionar_zonas, name='gestionar_zonas'),
    path('editar-zona/<int:zona_id>/', views.editar_zona, name='editar_zona'),
    path('eliminar-zona/<int:zona_id>/', views.eliminar_zona, name='eliminar_zona'),
    path('editar-horario/<int:horario_id>/', views.editar_horario, name='editar_horario'),
    path('eliminar-horario/<int:horario_id>/', views.eliminar_horario, name='eliminar_horario'),
    path('gestionar-horarios/<int:zona_id>/', views.gestionar_horarios, name='gestionar_horarios'),
    path('lista-reservas-admin/', views.lista_reservas_admin, name='lista_reservas_admin'),
    path('reservas-hoy/', views.lista_reservas_hoy, name='lista_reservas_hoy'),
]