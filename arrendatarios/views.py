from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from usuarios.models import Usuario
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

    # CORRECCIÓN: usa 'desocupado' en lugar de "disponible"
    apartamentos = Apartamento.objects.filter(estado="desocupado")

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
        if residente_id:
            residente = get_object_or_404(User, id=residente_id)
            apartamento.ocupante_actual = residente
            # Opcional: cambia el estado a 'arrendado' si no lo está
            if apartamento.estado != 'arrendado':
                apartamento.estado = 'arrendado'
            apartamento.save()
            messages.success(request, f"Arrendatario actualizado para {apartamento.identificador}.")
            return redirect("arrendatarios:lista")
        else:
            messages.error(request, "Debe seleccionar un residente.")

    # Carga todos los residentes disponibles (puedes filtrar si quieres)
    residentes = User.objects.filter(rol="residente").order_by('first_name', 'last_name')

    return render(request, "arrendatarios/editar.html", {
        "apartamento": apartamento,
        "residentes": residentes,
        "residente_actual": apartamento.ocupante_actual,  # para pre-seleccionar
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


@login_required
def lista(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden ver esta lista.")
        return redirect('home')

    # Muestra TODOS los residentes que tengan apartamento en estado 'arrendado'
    # (o cambia el filtro si quieres ver todos los residentes)
    data = Usuario.objects.filter(
        rol='residente',
        apartamentos_ocupados__estado='arrendado'  # ← solo arrendados
    ).select_related('apartamentos_ocupados').order_by('apartamentos_ocupados__identificador')

    # Si quieres TODOS los residentes (incluso sin apartamento)
    # data = Usuario.objects.filter(rol='residente').select_related('apartamentos_ocupados').order_by('username')

    # Para el buscador por apartamento
    buscar = request.GET.get('buscar')
    if buscar:
        data = data.filter(apartamentos_ocupados__identificador__icontains=buscar)

    context = {
        'data': data,
    }

    return render(request, 'arrendatarios/lista.html', context)