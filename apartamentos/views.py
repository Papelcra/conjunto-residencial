from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Apartamento
from .forms import ApartamentoForm


@login_required
def apartamento_create(request):
    if not request.user.es_admin:
        raise PermissionDenied("Solo administradores pueden crear apartamentos.")

    if request.method == 'POST':
        form = ApartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Apartamento creado exitosamente.")
            return redirect('core:lista_apartamentos')
    else:
        form = ApartamentoForm()

    return render(request, 'apartamentos/apartamento_form.html', {
        'form': form,
        'titulo': 'Crear Nuevo Apartamento',
    })


@login_required
def apartamento_update(request, pk):
    if not request.user.es_admin:
        raise PermissionDenied("Solo administradores pueden editar apartamentos.")

    apartamento = get_object_or_404(Apartamento, pk=pk)

    if request.method == 'POST':
        form = ApartamentoForm(request.POST, instance=apartamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Apartamento actualizado exitosamente.")
            return redirect('core:lista_apartamentos')
    else:
        form = ApartamentoForm(instance=apartamento)

    return render(request, 'apartamentos/apartamento_form.html', {
        'form': form,
        'titulo': f'Editar Apartamento {apartamento.identificador}',
    })