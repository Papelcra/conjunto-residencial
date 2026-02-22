from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    # =============================
    # RESIDENTE
    # =============================
    path('notificar/', views.notificar_pago, name='notificar_pago'),
    path('mis-pagos/', views.mis_notificaciones, name='mis_notificaciones'),

    # 🔹 ESTA ES PARA EL RESIDENTE (NO LLEVA ID)
    path('estado-cuenta/', views.estado_cuenta_residente, name='estado_cuenta'),

    # =============================
    # ADMIN / SEGURIDAD
    # =============================
    path('estado-pagos/', views.estado_pagos, name='estado_pagos'),

    # 🔹 ESTA ES PARA ADMIN (CON ID)

    path('validar-pagos/', views.validar_pagos, name='validar_pagos'),
    path('aprobar-pago/<int:pago_id>/', views.aprobar_pago, name='aprobar_pago'),
    path('rechazar-pago/<int:pago_id>/', views.rechazar_pago, name='rechazar_pago'),

    path('historial/<int:apto_id>/', views.historial_pagos, name='historial_pagos'),
    path('reporte-pagos/', views.reporte_pagos, name='reporte_pagos'),

    path('registrar-pago/', views.registrar_pago, name='registrar_pago'),
    path('estado-cuenta-admin/<int:apto_id>/', views.estado_cuenta_admin, name='estado_cuenta_admin'),
    path('morosidad/', views.morosidad, name='morosidad'),
]