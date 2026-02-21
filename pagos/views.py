from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import NotificarPagoForm
from .models import Pago
from apartamentos.models import Apartamento
from django.utils import timezone


# =============================
# NOTIFICAR PAGO (RESIDENTE)
# =============================
@login_required
def notificar_pago(request):
    if not request.user.es_residente:
        messages.error(request, "Solo los residentes pueden notificar pagos.")
        return redirect('home')

    apartamento = getattr(request.user, "apartamento", None)

    if not apartamento:
        messages.error(request, "No tienes un apartamento asignado.")
        return redirect('home')

    if request.method == 'POST':
        form = NotificarPagoForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.apartamento = apartamento
            pago.residente = request.user
            pago.estado = 'pendiente'
            pago.save()
            messages.success(request, "Pago notificado correctamente.")
            return redirect('home')
    else:
        form = NotificarPagoForm()

    return render(request, "pagos/notificar_pago.html", {
        "form": form,
        "apartamento": apartamento
    })


# =============================
# ESTADO DE CUENTA (RESIDENTE)
# =============================
@login_required
def estado_cuenta(request):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes pueden ver su estado de cuenta.")
        return redirect('home')

    apartamento = getattr(request.user, "apartamento", None)

    if not apartamento:
        messages.error(request, "No tienes apartamento asignado.")
        return redirect('home')

    pagos = Pago.objects.filter(apartamento=apartamento).order_by('-fecha_pago')
    total_pagado = sum(p.monto for p in pagos if p.estado == 'aprobado')

    return render(request, "pagos/estado_cuenta.html", {
        "apartamento": apartamento,
        "pagos": pagos,
        "total_pagado": total_pagado
    })


# =============================
# ESTADO PAGOS (ADMIN)
# =============================
@login_required
def estado_pagos(request):
    # permisos
    if not (request.user.es_admin or request.user.es_seguridad):
        messages.error(request, "No tienes permiso.")
        return redirect('home')

    # traemos apartamentos (ajusta select_related si tu modelo referencia al usuario)
    apartamentos_qs = Apartamento.objects.all()

    hoy = timezone.localdate()  # usa timezone para compatibilidad

    apartamentos = []
    for apto in apartamentos_qs:
        # pagos aprobados para este apartamento
        pagos_aprobados = Pago.objects.filter(apartamento=apto, estado='aprobado')
        total_pagado = sum((p.monto or 0) for p in pagos_aprobados)

        # último pago aprobado (si existe)
        ultimo_aprobado = pagos_aprobados.order_by('-fecha_pago').first()

        # cálculo de meses desde último pago (si hay fecha)
        meses_vencidos = None
        al_dia = False
        if ultimo_aprobado and ultimo_aprobado.fecha_pago:
            last = ultimo_aprobado.fecha_pago
            meses_vencidos = (hoy.year - last.year) * 12 + (hoy.month - last.month)
            # regla simple: si hizo pago en el mes actual o el anterior => al día
            al_dia = meses_vencidos <= 1
        else:
            # sin pago aprobado -> moroso
            meses_vencidos = None
            al_dia = False

        # intento obtener el valor de administración si existe (para calcular deuda)
        valor_admin = getattr(apto, 'valor_admin', None) or getattr(apto, 'valor_mensual', None)

        if valor_admin is not None:
            # deuda estimada: si valor_admin es por mes y no conocemos meses, simplemente calcular diferencia
            deuda = max(0, valor_admin - total_pagado)
        else:
            deuda = None  # sin dato para calcular deuda

        # nombre de torre / bloque / sector (flexible)
        torre = getattr(apto, 'torre', None) or getattr(apto, 'bloque', None) or getattr(apto, 'torre_nombre', None) or "N/A"
        numero = getattr(apto, 'numero', None) or getattr(apto, 'codigo', None) or str(getattr(apto, 'id', ''))
        # inquilino / residente
        tenant_obj = getattr(apto, 'residente', None) or getattr(apto, 'arrendatario', None)
        tenant = str(tenant_obj) if tenant_obj else "Sin asignar"

        apartamentos.append({
            "id": apto.id,
            "torre": torre,
            "numero": numero,
            "tenant": tenant,
            "total_pagado": total_pagado,
            "deuda": deuda,
            "meses_vencidos": meses_vencidos,
            "al_dia": al_dia,
        })

    # puedes ordenar apartamentos si quieres (ej: por torre y número)
    apartamentos = sorted(apartamentos, key=lambda x: (x['torre'], x['numero']))

    return render(request, "pagos/estado_cuenta.html", {
        "apartamentos": apartamentos
    })


# =============================
# VALIDAR PAGOS (ADMIN)
# =============================
@login_required
def validar_pagos(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    pagos_pendientes = Pago.objects.filter(estado='pendiente').order_by('-creado_en')

    return render(request, "validar_pagos.html", {
        "pagos_pendientes": pagos_pendientes
    })


@login_required
def aprobar_pago(request, pago_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    pago = get_object_or_404(Pago, id=pago_id)
    pago.estado = 'aprobado'
    pago.save()

    messages.success(request, "Pago aprobado.")
    return redirect("pagos:validar_pagos")


@login_required
def rechazar_pago(request, pago_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    pago = get_object_or_404(Pago, id=pago_id)
    pago.estado = 'rechazado'
    pago.save()

    messages.success(request, "Pago rechazado.")
    return redirect("pagos:validar_pagos")


# =============================
# HISTORIAL PAGOS
# =============================
@login_required
def historial_pagos(request, apto_id):
    apartamento = get_object_or_404(Apartamento, id=apto_id)
    pagos = Pago.objects.filter(apartamento=apartamento).order_by('-fecha_pago')

    return render(request, "pagos/historial_pagos.html", {
        "apartamento": apartamento,
        "pagos": pagos
    })


# =============================
# MIS NOTIFICACIONES (RESIDENTE)
# =============================
@login_required
def mis_notificaciones(request):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes.")
        return redirect('home')

    pagos = Pago.objects.filter(residente=request.user).order_by('-creado_en')

    return render(request, "pagos/mis_notificaciones.html", {
        "pagos": pagos
    })


# =============================
# REPORTE TXT
# =============================
@login_required
def reporte_pagos(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    pagos = Pago.objects.all().order_by('-fecha_pago')

    texto = "REPORTE DE PAGOS\n\n"
    for p in pagos:
        texto += f"{p.apartamento} - {p.residente} - {p.monto} - {p.fecha_pago} - {p.estado}\n"

    response = HttpResponse(texto, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=reporte_pagos.txt"
    return response
# =============================
# REGISTRAR PAGO (ADMIN)
# =============================
@login_required
def registrar_pago(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden registrar pagos.")
        return redirect('home')

    messages.info(request, "Funcionalidad de registro manual en construcción.")
    return redirect("estado_pagos")