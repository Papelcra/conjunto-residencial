from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ZonaComun, Horario, Reserva


# Lista de zonas comunes (acceso para admin y residente)
@login_required
def lista_zonas(request):
    if not (request.user.es_admin or request.user.es_residente):
        messages.error(request, "No tienes permiso para ver zonas comunes.")
        return redirect('home')

    zonas = ZonaComun.objects.filter(disponible=True).prefetch_related('horarios')

    hoy = timezone.localdate()

    horarios_disponibles = []
    for zona in zonas:
        for horario in zona.horarios.all():
            reservada_hoy = Reserva.objects.filter(horario=horario, fecha=hoy, estado='aprobada').exists()
            horarios_disponibles.append({
                "horario": horario,
                "reservada_hoy": reservada_hoy
            })

    context = {
        'zonas': zonas,
        'horarios_disponibles': horarios_disponibles,  # lista plana para iterar en template
        'es_admin': request.user.es_admin
    }

    return render(request, "reservas/lista_zonas.html", context)

# Reservar horario (solo residentes)
@login_required
def reservar(request, horario_id):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes pueden reservar.")
        return redirect('reservas:lista_zonas')

    horario = get_object_or_404(Horario, id=horario_id)
    hoy = timezone.localdate()

    if Reserva.objects.filter(horario=horario, fecha=hoy).exists():
        messages.error(request, "Este horario ya está reservado para hoy.")
        return redirect('reservas:lista_zonas')

    reserva = Reserva(residente=request.user, horario=horario, fecha=hoy)
    reserva.save()
    messages.success(request, "Reserva realizada. Espera aprobación.")
    return redirect('reservas:mis_reservas')


# Mis reservas (solo residentes)
@login_required
def mis_reservas(request):
    if not request.user.es_residente:
        messages.error(request, "Solo residentes pueden ver sus reservas.")
        return redirect('home')

    reservas = Reserva.objects.filter(residente=request.user).order_by('-fecha')

    # Calcula los conteos aquí (en la vista)
    total_reservas = reservas.count()
    pendientes = reservas.filter(estado='pendiente').count()
    aprobadas = reservas.filter(estado='aprobada').count()
    canceladas = reservas.filter(estado='cancelada').count()

    context = {
        'reservas': reservas,
        'total_reservas': total_reservas,
        'pendientes': pendientes,
        'aprobadas': aprobadas,
        'canceladas': canceladas,
    }

    return render(request, "reservas/mis_reservas.html", context)

# Validar reservas (solo admin)
@login_required
def validar_reservas(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden validar reservas.")
        return redirect('home')

    reservas_pendientes = Reserva.objects.filter(estado='pendiente').order_by('-fecha')

    return render(request, "reservas/validar_reservas.html", {
        "reservas_pendientes": reservas_pendientes
    })


# Aprobar reserva (solo admin)
@login_required
def aprobar_reserva(request, reserva_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.estado = 'aprobada'
    reserva.save()

    messages.success(request, "Reserva aprobada.")
    return redirect('reservas:validar_reservas')


# Rechazar reserva (solo admin)
@login_required
def rechazar_reserva(request, reserva_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.estado = 'cancelada'
    reserva.save()

    messages.success(request, "Reserva rechazada.")
    return redirect('reservas:validar_reservas')

# Gestión de zonas comunes (solo admin)
@login_required
def gestionar_zonas(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden gestionar zonas comunes.")
        return redirect('home')

    zonas = ZonaComun.objects.all()

    if request.method == 'POST':
        # Crear nueva zona
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        capacidad = request.POST.get('capacidad', 1)
        disponible = request.POST.get('disponible') == 'on'

        if nombre:
            ZonaComun.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                capacidad=capacidad,
                disponible=disponible
            )
            messages.success(request, "Zona creada correctamente.")
            return redirect('reservas:gestionar_zonas')

    return render(request, 'reservas/gestionar_zonas.html', {
        'zonas': zonas
    })


# Editar zona (solo admin)
@login_required
def editar_zona(request, zona_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    zona = get_object_or_404(ZonaComun, id=zona_id)

    if request.method == 'POST':
        zona.nombre = request.POST.get('nombre', zona.nombre)
        zona.descripcion = request.POST.get('descripcion', zona.descripcion)
        zona.capacidad = request.POST.get('capacidad', zona.capacidad)
        zona.disponible = request.POST.get('disponible') == 'on'
        zona.save()
        messages.success(request, "Zona actualizada.")
        return redirect('reservas:gestionar_zonas')

    return render(request, 'reservas/editar_zona.html', {'zona': zona})


# Eliminar zona (solo admin)
@login_required
def eliminar_zona(request, zona_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('home')

    zona = get_object_or_404(ZonaComun, id=zona_id)
    zona.delete()
    messages.success(request, "Zona eliminada.")
    return redirect('reservas:gestionar_zonas')

@login_required
def editar_horario(request, horario_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('reservas:gestionar_zonas')

    horario = get_object_or_404(Horario, id=horario_id)

    if request.method == 'POST':
        horario.dia_semana = request.POST.get('dia_semana', horario.dia_semana)
        horario.hora_inicio = request.POST.get('hora_inicio', horario.hora_inicio)
        horario.hora_fin = request.POST.get('hora_fin', horario.hora_fin)
        horario.save()
        messages.success(request, "Horario actualizado.")
        return redirect('reservas:gestionar_horarios', zona_id=horario.zona.id)

    return render(request, 'reservas/editar_horario.html', {'horario': horario})


@login_required
def eliminar_horario(request, horario_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores.")
        return redirect('reservas:gestionar_zonas')

    horario = get_object_or_404(Horario, id=horario_id)
    zona_id = horario.zona.id
    horario.delete()
    messages.success(request, "Horario eliminado.")
    return redirect('reservas:gestionar_horarios', zona_id=zona_id)

@login_required
def gestionar_horarios(request, zona_id):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden gestionar horarios.")
        return redirect('reservas:gestionar_zonas')

    zona = get_object_or_404(ZonaComun, id=zona_id)
    horarios = zona.horarios.all()

    if request.method == 'POST':
        dia_semana = request.POST.get('dia_semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        if dia_semana and hora_inicio and hora_fin:
            Horario.objects.create(
                zona=zona,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            messages.success(request, "Horario agregado correctamente.")
            return redirect('reservas:gestionar_horarios', zona_id=zona.id)

    return render(request, 'reservas/gestionar_horarios.html', {
        'zona': zona,
        'horarios': horarios
    })

@login_required
def lista_reservas_admin(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden ver todas las reservas.")
        return redirect('home')

    reservas = Reserva.objects.all().order_by('-fecha', '-horario__hora_inicio')

    return render(request, 'reservas/lista_reservas_admin.html', {
        'reservas': reservas
    })