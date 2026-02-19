from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from .forms import NotificarPagoForm
from .models import Pago
from apartamentos.models import Apartamento
from usuarios.models import Usuario


# =============================
# VISTA REAL (TU VERSIÓN - MANTENERLA SIEMPRE)
# =============================
@login_required
def notificar_pago(request):
    if not request.user.es_residente:
        messages.error(request, "Solo los residentes pueden notificar pagos.")
        return redirect('home')

    try:
        apartamento = request.user.apartamento
    except AttributeError:
        apartamento = None

    if not apartamento:
        messages.error(request, "No tienes un apartamento asignado. Contacta a administración.")
        return redirect('home')

    if request.method == 'POST':
        form = NotificarPagoForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.apartamento = apartamento
            pago.residente = request.user
            pago.estado = 'pendiente'
            pago.save()
            messages.success(request, "Pago notificado exitosamente. Espera la verificación de la administración.")
            return redirect('home')
    else:
        form = NotificarPagoForm()

    return render(request, 'pagos/notificar_pago.html', {
        'form': form,
        'apartamento': apartamento,
    })


# =============================
# VISTAS DE DEVELOP - ADAPTADAS A MODELOS REALES (NO SIMULADAS)
# =============================
@login_required
def estado_cuenta(request):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes pueden ver su estado de cuenta.")
        return redirect('home')

    try:
        apartamento = request.user.apartamento
    except AttributeError:
        apartamento = None

    if not apartamento:
        messages.error(request, "No tienes apartamento asignado.")
        return redirect('home')

    pagos = Pago.objects.filter(apartamento=apartamento).order_by('-fecha_pago')
    total_pagado = sum(p.monto for p in pagos if p.estado == 'aprobado')

    return render(request, "pagos/estado_cuenta.html", {
        "apartamento": apartamento,
        "pagos": pagos,
        "total_pagado": total_pagado,
    })


@login_required
def estado_pagos(request):
    if not (request.user.es_admin or request.user.es_seguridad):
        messages.error(request, "No tienes permiso para ver estado de pagos.")
        return redirect('home')

    apartamentos = Apartamento.objects.all()
    estados = []
    for apto in apartamentos:
        pagos = Pago.objects.filter(apartamento=apto, estado='aprobado')
        total_pagado = sum(p.monto for p in pagos)
        # Puedes agregar lógica de deuda si tienes valor_admin en Apartamento
        deuda = 0  # calcula aquí si tienes modelo de cuotas

        estados.append({
            "apartamento": apto,
            "total_pagado": total_pagado,
            "deuda": deuda,
            "al_dia": deuda == 0,
        })

    return render(request, "pagos/estado_pagos.html", {
        "estados": estados,
    })


@login_required
def registrar_pago(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden registrar pagos.")
        return redirect('home')

    # Aquí iría formulario real para registrar pago (puedes crearlo después)
    messages.success(request, "Pago registrado (funcionalidad pendiente).")
    return redirect("estado_pagos")


@login_required
def historial_pagos(request, apto_id):
    apartamento = get_object_or_404(Apartamento, id=apto_id)
    pagos = Pago.objects.filter(apartamento=apartamento).order_by('-fecha_pago')

    return render(request, "pagos/historial_pagos.html", {
        "apartamento": apartamento,
        "pagos": pagos
    })


@login_required
def reporte_pagos(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden generar reportes.")
        return redirect('home')

    pagos = Pago.objects.all().order_by('-fecha_pago')
    texto = "REPORTE DE PAGOS\n\n"
    for p in pagos:
        texto += f"{p.apartamento.identificador} - {p.residente.get_full_name()} - {p.monto} - {p.fecha_pago} - {p.estado}\n"

    response = HttpResponse(texto, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=reporte_pagos.txt"
    return response


@login_required
def notificar_pagos(request):
    # Redirige a tu vista real
    return notificar_pago(request)


@login_required
def validar_pagos(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden validar pagos.")
        return redirect('home')

    pagos_pendientes = Pago.objects.filter(estado='pendiente').order_by('-creado_en')

    return render(request, "pagos/validar_pagos.html", {
        "pagos_pendientes": pagos_pendientes
    })


@login_required
def aprobar_pago(request, pago_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden aprobar pagos.")
        return redirect('home')

    pago = get_object_or_404(Pago, id=pago_id)
    pago.estado = 'aprobado'
    pago.save()
    messages.success(request, f"Pago {pago.id} aprobado.")
    return redirect("validar_pagos")


@login_required
def rechazar_pago(request, pago_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden rechazar pagos.")
        return redirect('home')

    pago = get_object_or_404(Pago, id=pago_id)
    pago.estado = 'rechazado'
    pago.save()
    messages.success(request, f"Pago {pago.id} rechazado.")
    return redirect("validar_pagos")


@login_required
def mis_notificaciones(request):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes pueden ver sus notificaciones.")
        return redirect('home')

    pagos = Pago.objects.filter(residente=request.user).order_by('-creado_en')

    return render(request, "pagos/mis_notificaciones.html", {
        "pagos": pagos
    })