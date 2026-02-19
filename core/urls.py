from django.urls import path
from . import views
from .views import dashboard_admin

app_name = 'core'

urlpatterns = [
    path('apartamentos/', views.lista_apartamentos, name='lista_apartamentos'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
]