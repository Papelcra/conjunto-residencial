from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils import timezone

from .forms import ReservaForm, ZonaComunForm
from .models import Reserva
from apartamentos.models import Apartamento
from pagos.views import calcular_meses_deuda


# ==========================================
# CREAR RESERVA
# ==========================================

@login_required
def crear_reserva(request):

    # 🔐 Solo residentes o admin pueden reservar
    if not (request.user.es_residente or request.user.es_admin):
        messages.error(request, "No tienes permiso para reservar.")
        return redirect("home")

    # 🔎 Validar pagos si es residente
    if request.user.es_residente:
        apartamento = Apartamento.objects.filter(
            ocupante_actual=request.user
        ).first()

        if not apartamento:
            messages.error(request, "No tienes apartamento asignado.")
            return redirect("home")

        meses_deuda = calcular_meses_deuda(apartamento)

        if meses_deuda > 0:
            messages.error(request, "No estás al día en pagos.")
            return redirect("home")

    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.residente = request.user

            try:
                reserva.full_clean()
                reserva.save()
                messages.success(request, "Reserva creada correctamente.")
                return redirect("zonas:calendario")
            except ValidationError as e:
                form.add_error(None, e)

    else:
        form = ReservaForm()

    return render(request, "zonas/crear.html", {"form": form})


# ==========================================
# CALENDARIO DE RESERVAS
# ==========================================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.safestring import mark_safe
import json

@login_required
def calendario_reservas(request):

    reservas = Reserva.objects.all()

   
    if request.user.es_seguridad:
        hoy = timezone.localdate()
        reservas = reservas.filter(fecha=hoy)

    eventos = []

    for reserva in reservas:
        eventos.append({
            "title": f"{reserva.zona.nombre} - {reserva.residente.get_full_name() or reserva.residente.username}",
            "start": f"{reserva.fecha}T{reserva.hora_inicio}",
            "end": f"{reserva.fecha}T{reserva.hora_fin}",
        })

    
    eventos_json = mark_safe(json.dumps(eventos))

    return render(request, "zonas/calendario.html", {
        "eventos": eventos_json
    })

# ==========================================
# CREAR ZONA (SOLO ADMIN)
# ==========================================

@login_required
def crear_zona(request):

    if not request.user.es_admin:
        messages.error(request, "No tienes permiso para crear zonas.")
        return redirect("home")

    if request.method == "POST":
        form = ZonaComunForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona común creada correctamente.")
            return redirect("zonas:crear_zona")
    else:
        form = ZonaComunForm()

    return render(request, "zonas/crear_zona.html", {"form": form})