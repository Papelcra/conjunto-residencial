from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime

# =============================
# DATOS SIMULADOS
# =============================
APARTAMENTOS = [
    {"id": 1, "numero": "101", "arrendatario": "Juan Pérez", "valor_admin": 100000},
    {"id": 2, "numero": "102", "arrendatario": "María Gómez", "valor_admin": 100000},
    {"id": 3, "numero": "201", "arrendatario": "Carlos Ruiz", "valor_admin": 120000},
]

PAGOS = [
    {"apartamento_id": 1, "fecha": "2026-01-10", "valor": 100000, "metodo": "Transferencia"},
    {"apartamento_id": 1, "fecha": "2026-02-10", "valor": 100000, "metodo": "Efectivo"},
    {"apartamento_id": 2, "fecha": "2026-01-15", "valor": 100000, "metodo": "Transferencia"},
]

# =============================
# LOGICA
# =============================
def calcular_estados():
    hoy = datetime.date.today()
    mes_actual = hoy.month
    estados = []

    for apto in APARTAMENTOS:
        pagos_apto = [p for p in PAGOS if p["apartamento_id"] == apto["id"]]
        total_pagado = sum(p["valor"] for p in pagos_apto)
        meses_pagados = int(total_pagado / apto["valor_admin"])

        meses_deuda = max(0, mes_actual - meses_pagados)
        al_dia = meses_deuda == 0

        estados.append({
            "apartamento": apto,
            "meses_deuda": meses_deuda,
            "al_dia": al_dia
        })

    return estados

# =============================
# VISTAS
# =============================

# ESTA YA LA USAS (NO SE TOCA)
def estado_cuenta(request):
    return render(request, "estado_cuenta.html")

# NUEVA VISTA PAGOS
def estado_pagos(request):
    estados = calcular_estados()
    return render(request, "estado_pagos.html", {
        "apartamentos": APARTAMENTOS,
        "estados": estados
    })

def registrar_pago(request):
    if request.method == "POST":
        PAGOS.append({
            "apartamento_id": int(request.POST.get("apartamento")),
            "fecha": request.POST.get("fecha"),
            "valor": int(request.POST.get("valor")),
            "metodo": request.POST.get("metodo"),
        })
    return redirect("estado_pagos")

def historial_pagos(request, apto_id):
    apto = next(a for a in APARTAMENTOS if a["id"] == apto_id)
    pagos = [p for p in PAGOS if p["apartamento_id"] == apto_id]

    return render(request, "historial_pagos.html", {
        "apartamento": apto,
        "pagos": pagos
    })

def reporte_pagos(request):
    texto = "REPORTE DE PAGOS (SIMULADO)\n\n"
    for p in PAGOS:
        apto = next(a for a in APARTAMENTOS if a["id"] == p["apartamento_id"])
        texto += f"Apto {apto['numero']} - {apto['arrendatario']} - {p['valor']} - {p['fecha']}\n"

    response = HttpResponse(texto, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=reporte_pagos.txt"
    return response
# ===== NOTIFICACIONES DE PAGO (SIMULADO) =====

NOTIFICACIONES = [
    {
        "id": 1,
        "apartamento": "101",
        "residente": "Juan Pérez",
        "fecha": "2026-02-10",
        "archivo": "comprobante1.jpg",
        "estado": "Pendiente"
    }
]


def notificar_pagos(request):
    if request.method == "POST":
        nueva = {
            "id": len(NOTIFICACIONES) + 1,
            "apartamento": request.POST.get("apartamento"),
            "residente": request.POST.get("residente"),
            "fecha": request.POST.get("fecha"),
            "archivo": request.POST.get("archivo"),
            "estado": "Pendiente"
        }
        NOTIFICACIONES.append(nueva)

    return render(request, "notificar_pagos.html", {
        "notificaciones": NOTIFICACIONES
    })


def validar_pagos(request):
    return render(request, "validar_pagos.html", {
        "notificaciones": NOTIFICACIONES
    })


def aprobar_pago(request, notif_id):
    for n in NOTIFICACIONES:
        if n["id"] == notif_id:
            n["estado"] = "Aprobado"
    return redirect("validar_pagos")


def rechazar_pago(request, notif_id):
    for n in NOTIFICACIONES:
        if n["id"] == notif_id:
            n["estado"] = "Rechazado"
    return redirect("validar_pagos")


def mis_notificaciones(request):
    return render(request, "mis_notificaciones.html", {
        "notificaciones": NOTIFICACIONES
    })
