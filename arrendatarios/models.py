from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from apartamentos.models import Apartamento
from pagos.models import Pago


@login_required
def lista_arrendatarios(request):
    if not (request.user.es_admin or request.user.es_seguridad):
        raise PermissionDenied("No tienes permiso para acceder aquí.")

    busqueda = request.GET.get('buscar')

    apartamentos = Apartamento.objects.filter(
        estado='arrendado'
    ).select_related('ocupante_actual')

    if busqueda:
        apartamentos = apartamentos.filter(
            identificador__icontains=busqueda
        )

    data = []

    for apto in apartamentos:
        ultimo_pago = Pago.objects.filter(
            apartamento=apto
        ).order_by('-fecha_pago').first()

        data.append({
            "apartamento": apto,
            "residente": apto.ocupante_actual,
            "estado_pago": ultimo_pago.estado if ultimo_pago else "Sin pagos",
        })

    return render(request, "arrendatarios/lista.html", {
        "data": data
    })
