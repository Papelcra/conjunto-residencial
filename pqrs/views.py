from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PQRS
from usuarios.decorators import solo_roles
from django.contrib import messages


@login_required
@solo_roles('admin', 'seguridad')
def listar_pqrs(request):
    pqrs = PQRS.objects.all().order_by('-fecha_creacion')
    return render(request, 'pqrs/listar.html', {'pqrs': pqrs})


@login_required
@solo_roles('residente')
def crear_pqrs(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        asunto = request.POST.get('asunto')
        descripcion = request.POST.get('descripcion')

        PQRS.objects.create(
            usuario=request.user,
            tipo=tipo,
            asunto=asunto,
            descripcion=descripcion
        )

        return redirect('mis_pqrs')  

    return render(request, 'pqrs/crear.html')

@login_required
@solo_roles('admin')
def responder_pqrs(request, id):
    pqrs = get_object_or_404(PQRS, id=id)

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        pqrs.respuesta = respuesta
        pqrs.estado = 'RESPONDIDO'
        pqrs.save()
        return redirect('listar_pqrs')

    return render(request, 'pqrs/responder.html', {'pqrs': pqrs})
from django.contrib.auth.decorators import login_required
from usuarios.decorators import solo_roles
from .models import PQRS

@login_required
@solo_roles('residente')
def mis_pqrs(request):
    pqrs = PQRS.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'pqrs/mis_pqrs.html', {'pqrs': pqrs})
@login_required
@solo_roles('admin')
def eliminar_pqrs(request, id):
    pqrs = get_object_or_404(PQRS, id=id)

    # Regla: solo se pueden eliminar las respondidas
    if pqrs.estado != 'RESPONDIDO':
        messages.error(request, 'Solo se pueden eliminar PQRS respondidas')
        return redirect('listar_pqrs')

    if request.method == 'POST':
        pqrs.delete()
        messages.success(request, 'PQRS eliminada correctamente')
        return redirect('listar_pqrs')

    return render(request, 'pqrs/eliminar.html', {'pqrs': pqrs})