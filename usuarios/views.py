from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import CrearUsuarioForm

User = get_user_model()


@login_required
def crear_usuario(request):
    """
    Permite al administrador crear usuarios desde la interfaz web.
    NO usa el panel de Django Admin.
    """

    # 🔒 Solo administradores del sistema
    if not request.user.es_admin:
        return HttpResponseForbidden("No tienes permisos para acceder aquí.")

    if request.method == "POST":
        form = CrearUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()

            messages.success(
                request,
                f"Usuario '{usuario.username}' creado correctamente."
            )

            # ✅ Redirige al dashboard (flujo natural del sistema)
            return redirect("core:dashboard_admin")

    else:
        form = CrearUsuarioForm()

    context = {
        "form": form,
        "titulo": "Crear nuevo usuario"
    }

    return render(request, "usuarios/crear_usuario.html", context)


@login_required
def lista_usuarios(request):
    """
    Vista para que el admin vea los usuarios creados en el sistema.
    """

    if not request.user.es_admin:
        return HttpResponseForbidden("No tienes permisos para acceder aquí.")

    usuarios = User.objects.all().order_by("-date_joined")

    context = {
        "usuarios": usuarios
    }

    return render(request, "usuarios/lista_usuarios.html", context)
