from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

from .forms import NotificarPagoForm
from .models import Pago
from apartamentos.models import Apartamento

def calcular_estado_apartamentos():
    hoy = timezone.localdate()

    apartamentos = Apartamento.objects.select_related('ocupante_actual').all()

    resultado = []

    for apto in apartamentos:
        usuario = apto.ocupante_actual

        pagos_aprobados = Pago.objects.filter(
            apartamento=apto,
            estado='aprobado'
        ).order_by('-fecha_pago')

        if pagos_aprobados.exists():
            ultimo_pago = pagos_aprobados.first().fecha_pago
            meses_deuda = (hoy.year - ultimo_pago.year) * 12 + (hoy.month - ultimo_pago.month)
        else:
            meses_deuda = 12  # nunca ha pagado

        resultado.append({
            'apartamento': apto,
            'usuario': usuario,
            'meses_deuda': max(0, meses_deuda)
        })

    return resultado

# ============================================================
# FUNCIÓN CENTRAL (LA CLAVE DE TODO)
# Calcula cuántos meses debe un apartamento
# ============================================================
def calcular_meses_deuda(apartamento):
    hoy = timezone.localdate()

    pagos_aprobados = Pago.objects.filter(
        apartamento=apartamento,
        estado='aprobado'
    ).order_by('-fecha_pago')

    if pagos_aprobados.exists():
        ultimo_pago = pagos_aprobados.first().fecha_pago
        meses = (hoy.year - ultimo_pago.year) * 12 + (hoy.month - ultimo_pago.month)
        return max(0, meses)
    else:
        # Nunca ha pagado
        return 12


# =============================
# NOTIFICAR PAGO (RESIDENTE)
# =============================
@login_required
def notificar_pago(request):
    if not request.user.es_residente:
        messages.error(request, "Solo los residentes pueden notificar pagos.")
        return redirect('home')

    apartamento = Apartamento.objects.filter(ocupante_actual=request.user).first()

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
def estado_cuenta_residente(request):
    apartamento = Apartamento.objects.filter(ocupante_actual=request.user).first()

    if not apartamento:
        messages.error(request, "No tienes un apartamento asignado.")
        return redirect('home')

    pagos = Pago.objects.filter(apartamento=apartamento)
    total_pagado = sum(p.monto for p in pagos if p.estado == 'aprobado')

    return render(request, "pagos/estado_cuenta.html", {
        "apartamento": apartamento,
        "pagos": pagos,
        "total_pagado": total_pagado
    })


# =============================
# ESTADO DE CUENTA (ADMIN)
# =============================
@login_required
def estado_cuenta_admin(request, apto_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden acceder.")
        return redirect('home')

    apartamento = get_object_or_404(Apartamento, id=apto_id)

    pagos = Pago.objects.filter(apartamento=apartamento).order_by('-fecha_pago')
    total_pagado = sum(p.monto for p in pagos if p.estado == "aprobado")

    return render(request, "pagos/estado_cuenta_admin.html", {
        "apartamento": apartamento,
        "pagos": pagos,
        "total_pagado": total_pagado
    })


# =============================
# PANEL GENERAL DE PAGOS (ADMIN)
# =============================
@login_required
def estado_pagos(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden acceder.")
        return redirect('home')

    data = calcular_estado_apartamentos()

    return render(request, 'pagos/estado_pagos.html', {
        'data': data
    })

# =============================
# MOROSIDAD (SOLO LOS QUE DEBEN)
# =============================
@login_required
def morosidad(request):
    if not (request.user.es_admin or request.user.es_seguridad):
        messages.error(request, "No tienes permiso.")
        return redirect('home')

    data = calcular_estado_apartamentos()

    morosos = [d for d in data if d['meses_deuda'] > 0]

    return render(request, 'pagos/morosidad.html', {
        'morosos': morosos
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

    return render(request, "pagos/validar_pagos.html", {
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
    return redirect("pagos:estado_pagos")