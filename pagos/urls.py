from django.urls import path
from . import views

app_name = 'pagos'   # ← ESTO ES OBLIGATORIO para usar 'pagos:nombre'

urlpatterns = [
    path('notificar/', views.notificar_pago, name='notificar'),
    # Puedes agregar más rutas después
]