# =============================================
# IMPORTS
# =============================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Modelos y forms
from .models import Usuario, RecuperacionSolicitud
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import SetPasswordForm


# =============================================
# CREAR USUARIO (solo admin)
# =============================================
@staff_member_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario '{user.username}' creado como {user.get_rol_display()}.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})


# =============================================
# LISTA DE RESIDENTES (admin y seguridad)
# =============================================
@login_required
def lista_residentes(request):
    if not (request.user.es_admin or request.user.es_seguridad):
        messages.error(request, "No tienes permiso para ver la lista de residentes.")
        return redirect('home')

    residentes = Usuario.objects.filter(rol='residente').select_related('apartamento').order_by('first_name', 'last_name')

    return render(request, 'usuarios/lista_residentes.html', {
        'residentes': residentes
    })


# =============================================
# SOLICITUD DE RECUPERACIÓN DE CONTRASEÑA
# =============================================
def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Siempre mostramos éxito (seguridad: no revelamos si el email existe)
            messages.success(request, "Solicitud enviada correctamente. El administrador te contactará pronto.")
            
            # Intentamos crear la solicitud solo si el usuario existe
            try:
                usuario = Usuario.objects.get(email=email)
                RecuperacionSolicitud.objects.create(
                    usuario=usuario,
                    email=email
                )
                # Envía correo al admin
                send_mail(
                    subject='Nueva solicitud de recuperación de contraseña',
                    message=f'El usuario {usuario.username} ({email}) solicitó recuperar su contraseña.\n\n'
                            f'Fecha y hora: {timezone.now().strftime("%d/%m/%Y %H:%M")}\n'
                            f'IP: {request.META.get("REMOTE_ADDR", "No disponible")}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['tuemailreal@dominio.com'],  # ← CAMBIA POR TU CORREO
                    fail_silently=False,
                )
            except Usuario.DoesNotExist:
                # No hacemos nada más, pero el usuario ve el mensaje de éxito igual
                pass
        else:
            messages.error(request, "Por favor ingresa tu correo electrónico.")

    return render(request, 'usuarios/recuperar.html')


# =============================================
# SOLICITUDES DE RECUPERACIÓN (para admin)
# =============================================
@login_required
def solicitudes_recuperacion(request):
    if not request.user.es_admin:
        messages.error(request, "Solo administradores pueden ver estas solicitudes.")
        return redirect('home')

    solicitudes = RecuperacionSolicitud.objects.filter(procesada=False).order_by('-fecha_solicitud')

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        solicitud = get_object_or_404(RecuperacionSolicitud, id=solicitud_id)

        form = SetPasswordForm(user=solicitud.usuario, data=request.POST)
        if form.is_valid():
            form.save()
            solicitud.procesada = True
            solicitud.fecha_procesada = timezone.now()
            solicitud.save()
            messages.success(request, f"Contraseña cambiada para {solicitud.usuario.username} y solicitud marcada como procesada.")
        else:
            messages.error(request, "Error al cambiar la contraseña. Revisa los campos.")
    else:
        form = None

    return render(request, 'usuarios/solicitudes_recuperacion.html', {
        'solicitudes': solicitudes,
        'form': form,
    })


# =============================================
# PANEL RESIDENTE (CON CARRUSEL SIMULADO - de develop)
# =============================================
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