from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Usuario

@staff_member_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario '{user.username}' creado como {user.get_rol_display()}.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required
def lista_residentes(request):
    if not (request.user.es_admin or request.user.es_seguridad):
        messages.error(request, "No tienes permiso para ver la lista de residentes.")
        return redirect('home')

    residentes = Usuario.objects.filter(rol='residente').order_by('first_name')

    return render(request, 'usuarios/lista_residentes.html', {
        'residentes': residentes
    })