from .views import estado_cuenta
from django.urls import path

urlpatterns = [
    path('estado_cuenta/', estado_cuenta, name='estado_cuenta'),
]