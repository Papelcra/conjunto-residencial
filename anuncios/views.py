from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Anuncio
from .forms import AnuncioForm

# ===== LISTA =====
@login_required
def admin_lista_anuncios(request):
    anuncios = Anuncio.objects.order_by("-fecha_publicacion")
    return render(request, "anuncios/admin_lista_anuncio.html", {
        "anuncios": anuncios
    })

# ===== CREAR =====
@login_required
def crear_anuncio(request):
    if request.method == "POST":
        form = AnuncioForm(request.POST)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.creado_por = request.user
            anuncio.save()
            return redirect("admin_lista_anuncios")
    else:
        form = AnuncioForm()

    return render(request, "anuncios/crear_anuncio.html", {
        "form": form
    })

# ===== EDITAR =====
@login_required
def editar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)

    if request.method == "POST":
        form = AnuncioForm(request.POST, instance=anuncio)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.creado_por = request.user
            anuncio.save()
            return redirect("admin_lista_anuncios")
    else:
        form = AnuncioForm(instance=anuncio)

    return render(request, "anuncios/editar_anuncio.html", {
        "form": form
    })

# ===== ELIMINAR =====
@login_required
def eliminar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)

    if request.method == "POST":
        anuncio.delete()
        return redirect("admin_lista_anuncios")

    return render(request, "anuncios/eliminar_anuncio.html", {
        "anuncio": anuncio
    })