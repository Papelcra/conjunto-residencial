from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('apartamentos/', views.lista_apartamentos, name='lista_apartamentos'),
]