from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from anuncios.models import Anuncio


@login_required
def dashboard(request):
    request.user.refresh_from_db()

    # anuncios visibles para todos
    anuncios = Anuncio.objects.order_by("-destacado", "-fecha_publicacion")

    if request.user.rol == 'admin':
        template = 'dashboard_admin.html'
    elif request.user.rol == 'seguridad':
        template = 'dashboard_seguridad.html'
    else:
        template = 'dashboard_residente.html'

    return render(request, template, {
        'user': request.user,
        'anuncios': anuncios
    })