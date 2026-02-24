from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm


# ==========================
# CREAR USUARIO (ADMIN)
# ==========================
@staff_member_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Usuario '{user.username}' creado como {user.get_rol_display()}."
            )
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})


# ==========================
# PANEL RESIDENTE (CON CARRUSEL SIMULADO)
# ==========================
def panel_residente(request):

    anuncios = [
        {
            "titulo": "Corte de agua programado",
            "descripcion": "El martes 10:00 AM se realizará mantenimiento.",
            "imagen": "https://via.placeholder.com/900x350?text=Corte+de+agua"
        },
        {
            "titulo": "Reunión de copropietarios",
            "descripcion": "Asamblea general el sábado 6:00 PM.",
            "imagen": "https://via.placeholder.com/900x350?text=Asamblea"
        },
        {
            "titulo": "Mantenimiento ascensor",
            "descripcion": "El ascensor torre B estará fuera de servicio.",
            "imagen": "https://via.placeholder.com/900x350?text=Ascensor"
        }
    ]

    return render(request, "usuarios/dashboard_residente.html", {
        "anuncios": anuncios
    })