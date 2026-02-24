from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from apartamentos.models import Apartamento
from anuncios.models import Anuncio
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy

@login_required
def lista_apartamentos(request):
    # Solo admin y seguridad pueden ver esta página
    if not (request.user.es_admin or request.user.es_seguridad):
        raise PermissionDenied("No tienes permiso para ver esta página.")

    # Obtenemos todos los apartamentos ordenados
    apartamentos = Apartamento.objects.all().select_related('ocupante_actual')

    # Filtros opcionales por GET (por ejemplo ?estado=desocupado)
    estado_filtro = request.GET.get('estado')
    if estado_filtro:
        apartamentos = apartamentos.filter(estado=estado_filtro)

    # Contexto para el template
    context = {
        'apartamentos': apartamentos,
        'es_admin': request.user.es_admin,
        'estados': Apartamento.ESTADO_VIVIENDA,  # para el filtro en el template
    }

    return render(request, 'core/lista_apartamentos.html', context)



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # o '/accounts/login/'

    def dispatch(self, request, *args, **kwargs):
        # Mensaje opcional (queda muy bien)
        messages.success(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!")
        return super().dispatch(request, *args, **kwargs)


@login_required
def dashboard(request):
    request.user.refresh_from_db()

    anuncios = Anuncio.objects.order_by("-fecha_publicacion")

    if request.user.rol == 'admin':
        template = 'dashboard_admin.html'
    elif request.user.rol == 'seguridad':
        template = 'dashboard_seguridad.html'
    else:
        template = 'dashboard_residente.html'

    context = {
        'user': request.user,
        'anuncios': anuncios
    }

    return render(request, template, context)

@login_required
def dashboard_residente(request):
    anuncios = Anuncio.objects.order_by("-fecha_publicacion")

    context = {
        'user': request.user,
        'anuncios': anuncios
    }

    return render(request, 'dashboard_residente.html', context)