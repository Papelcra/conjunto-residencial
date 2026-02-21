from django.urls import path
from . import views

app_name = 'pagos'  # ← MANTENERLO: es obligatorio para nombres como 'pagos:notificar'

urlpatterns = [
    # Ruta original tuya (la mantenemos)
    path('notificar/', views.notificar_pago, name='notificar'),

    # Todas las rutas nuevas de develop (no se pierde ninguna)
    path("estado-cuenta/", views.estado_cuenta, name="estado_cuenta"),
    path("estado-pagos/", views.estado_pagos, name="estado_pagos"),
    path("registrar-pago/", views.registrar_pago, name="registrar_pago"),
    path("historial/<int:apto_id>/", views.historial_pagos, name="historial_pagos"),
    path("reporte-pagos/", views.reporte_pagos, name="reporte_pagos"),
    path("notificar-pagos/", views.notificar_pago, name="notificar_pago"),
    path("validar-pagos/", views.validar_pagos, name="validar_pagos"),
    path("aprobar-pago/<int:notif_id>/", views.aprobar_pago, name="aprobar_pago"),
    path("rechazar-pago/<int:notif_id>/", views.rechazar_pago, name="rechazar_pago"),
    path("mis-pagos/", views.mis_notificaciones, name="mis_notificaciones"),
]