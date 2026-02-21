from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from apartamentos.models import Apartamento
from pagos.models import Pago
from django.contrib import messages

User = get_user_model()


# 🔐 Verificar si es admin
def es_admin(user):
    return user.is_authenticated and user.es_admin


# ==========================================
# 📋 LISTA DE ARRENDATARIOS
# ==========================================

@login_required
def lista_arrendatarios(request):
    if not (request.user.es_admin or request.user.es_seguridad):
        raise PermissionDenied("No tienes permiso para acceder aquí.")

    apartamentos = Apartamento.objects.filter(
        estado='arrendado'
    ).select_related('ocupante_actual')

    data = []

    for apto in apartamentos:
        ultimo_pago = Pago.objects.filter(
            apartamento=apto
        ).order_by('-fecha_pago').first()

        data.append({
            "id": apto.id,  # 🔥 IMPORTANTE para editar/eliminar
            "apartamento": apto,
            "residente": apto.ocupante_actual,
            "estado_pago": ultimo_pago.estado if ultimo_pago else "Sin pagos",
        })

    return render(request, "arrendatarios/lista.html", {
        "data": data
    })


# ==========================================
# ➕ CREAR ARRENDATARIO
# ==========================================

@login_required
@user_passes_test(es_admin)
def crear_arrendatario(request):
    if request.method == "POST":
        apartamento_id = request.POST.get("apartamento")
        residente_id = request.POST.get("residente")

        apartamento = get_object_or_404(Apartamento, id=apartamento_id)
        residente = get_object_or_404(User, id=residente_id)

        apartamento.ocupante_actual = residente
        apartamento.estado = "arrendado"
        apartamento.save()
        messages.success(request, "Arrendatario asignado correctamente.")
        return redirect("arrendatarios:lista")

    apartamentos = Apartamento.objects.filter(estado="disponible")
    residentes = User.objects.filter(rol="residente")

    return render(request, "arrendatarios/crear.html", {
        "apartamentos": apartamentos,
        "residentes": residentes
    })


# ==========================================
# ✏ EDITAR ARRENDATARIO
# ==========================================

@login_required
@user_passes_test(es_admin)
def editar_arrendatario(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)

    if request.method == "POST":
        residente_id = request.POST.get("residente")
        residente = get_object_or_404(User, id=residente_id)

        apartamento.ocupante_actual = residente
        apartamento.save()
        messages.warning(request, "Arrendatario actualizado correctamente.")
        return redirect("arrendatarios:lista")

    residentes = User.objects.filter(rol="residente")

    return render(request, "arrendatarios/editar.html", {
        "apartamento": apartamento,
        "residentes": residentes
    })


# ==========================================
# ❌ ELIMINAR ARRENDATARIO
# ==========================================

@login_required
@user_passes_test(es_admin)
def eliminar_arrendatario(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)

    if request.method == "POST":
        apartamento.ocupante_actual = None
        apartamento.estado = "disponible"
        apartamento.save()
        messages.error(request, "Arrendatario eliminado correctamente.")
        return redirect("arrendatarios:lista")

    return render(request, "arrendatarios/eliminar.html", {
        "apartamento": apartamento
    })
