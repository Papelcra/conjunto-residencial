from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Mantenimiento
from .forms import MantenimientoForm
from apartamentos.models import Apartamento
from django.contrib import messages


# ==============================
# RESIDENTE CREA SOLICITUD
# ==============================
@login_required
def residente_crear(request):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes pueden solicitar mantenimiento.")
        return redirect('home')

    # Obtén el apartamento del residente actual (usa la property que ya tienes)
    apartamento = request.user.apartamento  # Esto devuelve el Apartamento o None

    if request.method == "POST":
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.residente = request.user
            mantenimiento.apartamento = apartamento  # Asigna automáticamente
            mantenimiento.save()
            messages.success(request, "Solicitud de mantenimiento enviada correctamente.")
            return redirect("mantenimientos:residente_lista")
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form = MantenimientoForm()

    return render(request, "mantenimientos/residente_crear.html", {
        "form": form,
        "apartamento": apartamento,  # ← PASAMOS EL APARTAMENTO AL TEMPLATE
    })


# ==============================
# RESIDENTE VE SUS SOLICITUDES
# ==============================
@login_required
def residente_lista(request):
    solicitudes = Mantenimiento.objects.filter(residente=request.user).order_by("-fecha_solicitud")
    return render(request, "mantenimientos/residente_lista.html", {
        "solicitudes": solicitudes
    })


# ==============================
# ADMIN VE TODAS
# ==============================
@login_required
def admin_lista(request):
    mantenimientos = Mantenimiento.objects.all().order_by("-fecha_solicitud")
    return render(request, "mantenimientos/admin_lista.html", {
        "mantenimientos": mantenimientos
    })


# ==============================
# ADMIN EDITA ESTADO
# ==============================
@login_required
def admin_editar(request, pk):
    mantenimiento = get_object_or_404(Mantenimiento, pk=pk)

    if request.method == "POST":
        mantenimiento.estado = request.POST.get("estado")
        mantenimiento.respuesta_admin = request.POST.get("respuesta_admin")
        mantenimiento.save()
        return redirect("mantenimientos:admin_lista")

    return render(request, "mantenimientos/admin_editar.html", {
        "mantenimiento": mantenimiento
    })