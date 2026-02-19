from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NotificarPagoForm
from .models import Pago


@login_required
def notificar_pago(request):
    if not request.user.es_residente:
        messages.error(request, "Solo los residentes pueden notificar pagos.")
        return redirect('home')

    # Intentamos obtener el apartamento asignado al residente
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