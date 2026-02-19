from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

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